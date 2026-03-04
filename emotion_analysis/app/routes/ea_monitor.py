import os
from typing import Any, Dict, Optional
from datetime import datetime
import boto3
from httpx import request
import numpy as np
from evidently import DataDefinition, Dataset, Report
from evidently.presets import DataDriftPreset, ClassificationPreset
from fastapi import APIRouter, Query
import pandas as pd
from pydantic import BaseModel
from shared.src.data.models.s3_config_model import S3ClientConfigModel, S3ConfigReadModel, S3ConfigWriteFileModel
from shared.src.data.helpers.aws_s3_helper import AwsS3Helper
from shared.src.common.env_constants import EnvConstants
from prometheus_client import Gauge

ea_monitor_router = APIRouter(tags=["ea_monitoring"])

BUFFER_SIZE = 100
TOP_N_FEATURES = 50  # Must match the value in ea_online_serving.py

data_drift_buffer = []
model_prediction_buffer = []

# ← Cache reference features đã được vectorize sẵn
_reference_features_cache: Optional[pd.DataFrame] = None

# Prometheus metrics
drift_detected = Gauge("ea_data_drift_dataset_drift", "1 if drift detected", ["dataset_name"])
drift_score = Gauge("ea_data_drift_share_drifted_features", "Ratio of drift features", ["dataset_name"])
drifted_features = Gauge("ea_data_drift_n_drifted_features", "Number of drifted features", ["dataset_name"])
classification_quality = Gauge("ea_classification_performance_quality", "Classification quality metrics", ["dataset", "metric"])

class GetModelPerformanceRequest(BaseModel):
    file_path: str  # S3 URI của file chứa predictions và targets, ví dụ: s3://bucket/path/to/eval_data.csv


def _get_aws_clients():
    s3_bucket = os.getenv(EnvConstants.AWS_S3_BUCKET)
    access_key = os.getenv(EnvConstants.AWS_ACCESS_KEY_ID)
    secret_key = os.getenv(EnvConstants.AWS_SECRET_ACCESS_KEY)
    ssm = boto3.client(
        "ssm",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="ap-southeast-1",
    )
    return s3_bucket, access_key, secret_key, ssm


async def build_reference_features(vectorizer) -> None:
    """
    Gọi 1 lần lúc startup: đọc raw training data từ S3,
    transform qua vectorizer, lấy top-N features, cache lại.
    """
    global _reference_features_cache

    s3_bucket, access_key, secret_key, ssm = _get_aws_clients()

    reference_file_name = ssm.get_parameter(
        Name="/emotion_analysis/pipeline/training_pipelines/ea_train_data"
    )["Parameter"]["Value"]

    raw_df = AwsS3Helper.read_data_from_s3(
        S3ConfigReadModel(
            s3_uri=f"s3://{s3_bucket}/emotion-analysis/{reference_file_name}",
            access_key=access_key,
            secret_key=secret_key,
        )
    )
    raw_df = raw_df.head(BUFFER_SIZE)

    # Transform text → TF-IDF sparse matrix
    texts = raw_df["cleaned_text"].tolist()
    features_sparse = vectorizer.transform(texts)  # (n_samples, n_vocab)

    # Lấy top-N features theo mean score — giống hệt logic trong ea_online_serving.py
    col_means = np.asarray(features_sparse.mean(axis=0)).flatten()
    top_indices = col_means.argsort()[-TOP_N_FEATURES:][::-1]
    top_features = features_sparse[:, top_indices].toarray()  # (n_samples, TOP_N_FEATURES)

    feat_cols = [f"feat_{i+1}" for i in range(TOP_N_FEATURES)]
    _reference_features_cache = pd.DataFrame(top_features, columns=feat_cols)
    print(f"[INFO] Reference features cached: shape={_reference_features_cache.shape}")


# Xóa 2 dòng global report objects cũ:
# data_drift_report = Report(metrics=[DataDriftPreset()])
# model_performance_report = Report(metrics=[ClassificationPreset()])


def run_data_drift_monitoring(
    reference_data: pd.DataFrame, current_data: pd.DataFrame
) -> Dict[str, Any]:
    # v0.7: Report nhận list, .run() trả về snapshot object
    report = Report([DataDriftPreset()])
    snapshot = report.run(current_data, reference_data)  # ← (current, reference)
    result_dict = snapshot.dict()                        # ← .dict() trên snapshot

    # Parse kết quả từ structure mới
    metrics = result_dict.get("metrics", [])
    n_drifted = 0
    n_cols = 1
    for m in metrics:
        if "number_of_drifted_columns" in str(m):
            result = m.get("result", {})
            n_drifted = result.get("number_of_drifted_columns", 0)
            n_cols = result.get("number_of_columns", 1)
            break

    score = n_drifted / max(n_cols, 1)
    is_drift = score > 0

    drift_detected.labels(dataset_name="emotion_analysis").set(1 if is_drift else 0)
    drift_score.labels(dataset_name="emotion_analysis").set(score)
    drifted_features.labels(dataset_name="emotion_analysis").set(n_drifted)

    return {
        "drift": {
            "is_drift": is_drift,
            "drift_score": score,
            "n_drifted_features": n_drifted,
        }
    }


from evidently import DataDefinition, Dataset, Report
from evidently import MulticlassClassification  # hoặc BinaryClassification
from evidently.presets import ClassificationPreset


def run_model_performance_monitoring(
    predictions: list,
    targets: list,
) -> Dict[str, Any]:
    eval_df = pd.DataFrame({
        "target": [str(t) for t in targets],       # phải là string
        "prediction": [str(p) for p in predictions],  # phải là string
    })

    data_definition = DataDefinition(
        classification=[
            MulticlassClassification(
                target="target",
                prediction_labels="prediction",
            )
        ]
    )

    current_dataset = Dataset.from_pandas(eval_df, data_definition=data_definition)
    reference_dataset = Dataset.from_pandas(eval_df, data_definition=data_definition)

    report = Report([ClassificationPreset()])
    snapshot = report.run(current_dataset, reference_dataset)
    result_dict = snapshot.dict()

    current_metrics = {}
    for m in result_dict.get("metrics", []):
        result = m.get("result", {})
        if "current" in result:
            current_metrics = result["current"]
            break

    acc = current_metrics.get("accuracy", 0)
    f1 = current_metrics.get("f1", 0)

    classification_quality.labels(dataset="current", metric="accuracy").set(acc)
    classification_quality.labels(dataset="current", metric="f1").set(f1)

    return {"performance": {"accuracy": acc, "f1_score": f1}}

class EAMonitoring:
    @staticmethod
    @ea_monitor_router.get("/data-drift")
    async def detect_data_drift():
        s3_bucket = os.getenv(EnvConstants.AWS_S3_BUCKET)
        access_key = os.getenv(EnvConstants.AWS_ACCESS_KEY_ID)
        secret_key = os.getenv(EnvConstants.AWS_SECRET_ACCESS_KEY)

        ssm = boto3.client(
            'ssm',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='ap-southeast-1'
        )
        
        prediction_file_name = ssm.get_parameter(Name="/emotion_analysis/predictions")['Parameter']['Value']
        
        if not prediction_file_name:
            raise Exception("File not exist")
        
        prediction_df = AwsS3Helper.read_data_from_s3(
            S3ConfigReadModel(
                s3_uri=f"s3://{s3_bucket}/emotion-analysis/predictions/{prediction_file_name}",
                access_key=access_key,
                secret_key=secret_key
            )
        )
        
        if len(prediction_df) < 100:
            raise Exception("Current data not enough for monitoring")
        monitoring_results = run_data_drift_monitoring(
            reference_data=_reference_features_cache,
            current_data=prediction_df.drop(columns=["text", "prediction", "target"]),
        )
        print(f"[INFO] Data drift results: {monitoring_results}")
        return monitoring_results
    
    @staticmethod
    @ea_monitor_router.get("/model-performance")
    async def monitor_model_performance(
    file_path: str = Query(..., description="S3 URI of prediction file, e.g. s3://bucket/path/eval.csv")
):
        s3_bucket = os.getenv(EnvConstants.AWS_S3_BUCKET)
        access_key = os.getenv(EnvConstants.AWS_ACCESS_KEY_ID)
        secret_key = os.getenv(EnvConstants.AWS_SECRET_ACCESS_KEY)
        
        if file_path.startswith("s3://"):
            prediction_df = AwsS3Helper.read_data_from_s3(
                S3ConfigReadModel(
                    s3_uri=file_path,
                    access_key=access_key,
                    secret_key=secret_key
                )
            )       
        
            if len(prediction_df) < 100:
                raise Exception("Current data not enough for monitoring")
            if prediction_df["target"].isnull().any():
                raise Exception("Targets need to be available for performance monitoring")

            monitoring_results = run_model_performance_monitoring(
                predictions=prediction_df["prediction"].tolist(),
                targets=prediction_df["target"].tolist(),
            )
            print(f"[INFO] Model performance results: {monitoring_results}")
            return monitoring_results
        else:
            raise ValueError("Unsupported file format. Please provide an S3 URI.")