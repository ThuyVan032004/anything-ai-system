import os

import boto3
from fastapi import APIRouter
import httpx
import numpy as np
import pandas as pd
from shared.src.common.env_constants import EnvConstants
from shared.src.data.helpers.aws_s3_helper import AwsS3Helper
from shared.src.data.models.s3_config_model import S3ClientConfigModel, S3ConfigReadModel, S3ConfigWriteFileModel

from emotion_analysis.data.ea_data_cleaning import EATextDataCleaning
from emotion_analysis.data.helpers.text_data_cleaning_helper import TextDataCleaningHelper

ea_prediction_router = APIRouter(tags=["ea_online_serving"])

MONITORING_BASE_URL = "http://monitoring-service:8767"
TOP_N_FEATURES = 50  # Must match the value in ea_monitoring.py


def _extract_top_features(features_sparse, n: int = TOP_N_FEATURES) -> list:
    """
    Convert sparse TF-IDF matrix to a dense list of lists with only the top-N
    features (by mean score across samples) to avoid MemoryError on large vocabs.

    Returns: list of lists, shape [n_samples, n]
    """
    # Compute column-wise mean to find globally important features
    # .mean(axis=0) returns a (1, n_vocab) matrix → flatten to 1-D array
    col_means = np.asarray(features_sparse.mean(axis=0)).flatten()
    top_indices = col_means.argsort()[-n:][::-1]  # indices of top-N cols

    # Slice only those columns (still sparse), then convert to dense
    top_features = features_sparse[:, top_indices].toarray()  # (n_samples, n)
    return top_features.tolist()


async def _send_to_monitoring() -> None:
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{MONITORING_BASE_URL}/data-drift",
                timeout=5.0,
            )

        # await client.post(
        #     f"{MONITORING_BASE_URL}/model-performance",
        #     timeout=5.0,
        # )
    except Exception as e:
        print(f"[WARNING] Could not send data to monitoring service: {e}")


class EAOnlineServing:
    # @staticmethod
    # @ea_prediction_router.post("/predict")
    # async def predict(input_text: str):
    #     from emotion_analysis.main import model_pipeline

    #     ea_text_cleaner = EATextDataCleaning()
    #     cleaned_text = TextDataCleaningHelper.clean_text(
    #         text=input_text, cleaner=ea_text_cleaner
    #     )

    #     result = model_pipeline.predict([cleaned_text])

    #     vectorizer = model_pipeline.named_steps["vectorizer"]
    #     features = vectorizer.transform([cleaned_text])  # sparse (1, n_vocab)

    #     # FIX: slice to TOP_N_FEATURES before converting to dense → no MemoryError
    #     features_list = _extract_top_features(features)  # [[f0, f1, ..., f49]]

    #     async with httpx.AsyncClient() as client:
    #         await _send_to_monitoring(
    #             client=client,
    #             features_list=features_list,
    #             texts=input_text,
    #             predictions=int(result[0]),
    #         )

    #     return {"result": int(result[0])}

    @staticmethod
    @ea_prediction_router.post("/predict-many")
    async def predict_many(file_path: str):
        print(f"[INFO] Received file for prediction: {file_path}")
        if file_path.endswith(".csv"):
            data_frame = pd.read_csv(file_path)
        elif file_path.startswith("s3://"):
            s3_bucket = os.getenv(EnvConstants.AWS_S3_BUCKET)
            access_key = os.getenv(EnvConstants.AWS_ACCESS_KEY_ID)
            secret_key = os.getenv(EnvConstants.AWS_SECRET_ACCESS_KEY)

            data_frame = AwsS3Helper.read_data_from_s3(
                S3ConfigReadModel(
                    s3_uri=file_path,
                    access_key=access_key,
                    secret_key=secret_key
                )
            )
        else:
            raise ValueError("Unsupported file format.")
        
        from emotion_analysis.main import model_pipeline

        ea_text_cleaner = EATextDataCleaning()
        cleaned_texts = [
            TextDataCleaningHelper.clean_text(text=text, cleaner=ea_text_cleaner)
            for text in data_frame["text"]
        ]
        result = model_pipeline.predict(cleaned_texts)

        vectorizer = model_pipeline.named_steps["vectorizer"]
        features = vectorizer.transform(cleaned_texts)  # sparse (n_samples, n_vocab)

        # FIX: slice to TOP_N_FEATURES before converting to dense → no MemoryError
        feature_list = _extract_top_features(features)  # [[...], [...], ...]

        ssm = boto3.client(
            'ssm',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='ap-southeast-1'
        )
        
        # ✅ Code mới - xử lý trường hợp parameter chưa tồn tại
        from botocore.exceptions import ClientError

        try:
            prediction_file_name = ssm.get_parameter(
                Name="/emotion_analysis/predictions"
            )['Parameter']['Value']
        except ClientError as e:
            if e.response['Error']['Code'] == 'ParameterNotFound':
                prediction_file_name = None
            else:
                raise  # Re-raise nếu là lỗi khác
            
        if not prediction_file_name:
            prediction_file_name = f"ea_predictions_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            transposed = list(zip(*feature_list))  # shape: (50 features, 100 samples)

            prediction_df = pd.DataFrame({
                "text": data_frame["text"],
                **{f"feat_{i+1}": list(transposed[i]) for i in range(TOP_N_FEATURES)},
                "prediction": result.tolist(),
                "target": [None] * len(result)
            })
                        
            prediction_df.to_csv(prediction_file_name, index=False)
            
            AwsS3Helper.upload_file_to_s3(
                S3ClientConfigModel(
                    access_key=access_key,
                    secret_key=secret_key
                ),
                S3ConfigWriteFileModel(
                    file_name=prediction_file_name,
                    s3_file_path=f"emotion-analysis/predictions/{prediction_file_name}",
                    s3_bucket_name=s3_bucket
                )
            )
            ssm.put_parameter(
                Name="/emotion_analysis/predictions",
                Value=prediction_file_name,
                Overwrite=True,
                Type="String"
            )
            
            # await _send_to_monitoring(client=httpx.AsyncClient())  # Gửi cả batch lên monitoring ngay lần đầu tiên
        else:
            prediction_df = AwsS3Helper.read_data_from_s3(
                S3ConfigReadModel(
                    s3_uri=f"s3://{s3_bucket}/emotion-analysis/predictions/{prediction_file_name}",
                    access_key=access_key,
                    secret_key=secret_key
                )
            )
            
            if len(prediction_df) >= 100:
                new_prediction_file_name = f"ea_predictions_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
                transposed = list(zip(*feature_list))  # shape: (50 features, 100 samples)

                new_prediction_df = pd.DataFrame({
                    "text": data_frame["text"],
                    **{f"feat_{i+1}": list(transposed[i]) for i in range(TOP_N_FEATURES)},
                    "prediction": result.tolist(),
                    "target": [None] * len(result)
                })
                
                new_prediction_df.to_csv(new_prediction_file_name, index=False)
                
                AwsS3Helper.upload_file_to_s3(
                    S3ClientConfigModel(
                        access_key=access_key,
                        secret_key=secret_key
                    ),
                    S3ConfigWriteFileModel(
                        file_name=new_prediction_file_name,
                        s3_file_path=f"emotion-analysis/predictions/{new_prediction_file_name}",
                        s3_bucket_name=s3_bucket
                    )
                )
                
                ssm.put_parameter(
                    Name="/emotion_analysis/predictions",
                    Value=new_prediction_file_name,
                    Overwrite=True,
                    Type="String"
                )
            else:
                transposed = list(zip(*feature_list))  # shape: (50 features, 100 samples)
                
                combined_df = pd.concat([prediction_df, pd.DataFrame({
                    "text": data_frame["text"],
                    **{f"feat_{i+1}": list(transposed[i]) for i in range(TOP_N_FEATURES)},
                    "prediction": result.tolist(),
                    "target": [None] * len(result)
                })], ignore_index=True)
                
                if len(combined_df) > 100:
                    combined_df = combined_df.tail(100)
                
                combined_df.to_csv(prediction_file_name, index=False)
        
        await _send_to_monitoring()  
                
        return  {
            text: int(prediction) for text, prediction in zip(data_frame["text"], result)
        }