import ast
import json
import os

import boto3
import joblib
import mlflow
from sklearn.pipeline import Pipeline

from emotion_analysis.common.constants import AppConstants
from emotion_analysis.models.helpers.ea_model_validation_helper import EAModelValidationHelper
from shared.src.common.env_constants import EnvConstants


if __name__ == "__main__":
    s3_bucket = os.getenv(EnvConstants.AWS_S3_BUCKET)
    access_key = os.getenv(EnvConstants.AWS_ACCESS_KEY_ID)
    secret_key = os.getenv(EnvConstants.AWS_SECRET_ACCESS_KEY)
    
    # Get test data file name from SSM Parameter Store
    ssm = boto3.client(
        'ssm',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='ap-southeast-1'
    )
    
    evaluation_report = ssm.get_parameter(Name="/emotion_analysis/pipeline/training_pipelines/ea_test_evaluation_report")['Parameter']['Value']
    evaluation_report_dict = json.loads(evaluation_report)
    
    # Get vectorizer file name from SSM Parameter Store
    vectorizer_file_name = ssm.get_parameter(Name="/emotion_analysis/pipeline/training_pipelines/ea_trained_vectorizer")['Parameter']['Value']
    
    run_id = ssm.get_parameter(Name="/emotion_analysis/mlflow/run_id")['Parameter']['Value']
    experiment_id = ssm.get_parameter(Name="/emotion_analysis/mlflow/experiment_id")['Parameter']['Value']
    model_file_name = ssm.get_parameter(Name="/emotion_analysis/pipeline/training_pipelines/ea_trained_model")['Parameter']['Value']
    vectorizer_file_name = ssm.get_parameter(Name="/emotion_analysis/pipeline/training_pipelines/ea_trained_vectorizer")['Parameter']['Value']
    

    mlflow.set_tracking_uri(AppConstants.MLFLOW_TRACKING_URI)

    # ✅ Download qua HTTP proxy — không dùng models:/ hay runs:/ URI
    model_path = mlflow.artifacts.download_artifacts(
        f"mlflow-artifacts:/{experiment_id}/{run_id}/artifacts/{model_file_name}",
    )
    vectorizer_path = mlflow.artifacts.download_artifacts(
        artifact_uri=f"mlflow-artifacts:/{experiment_id}/{run_id}/artifacts/{vectorizer_file_name}",
    )
    
    trained_model = joblib.load(model_path)
    trained_vectorizer = joblib.load(vectorizer_path)
    
    # Get evaluation metrics
    evaluation_metrics = {
        "accuracy": evaluation_report_dict["accuracy"],
        "precision_weighted": evaluation_report_dict["weighted avg"]["precision"],
        "recall_weighted": evaluation_report_dict["weighted avg"]["recall"],
        "f1_score_weighted": evaluation_report_dict["weighted avg"]["f1-score"]
    }
    
    print(f"Evaluation Metrics: {evaluation_metrics}")
    
    is_pass_thresholds = EAModelValidationHelper.validate_model_with_thresholds(evaluation_metrics)
    
    if is_pass_thresholds["result"]:
        print("Model passed validation thresholds and is ready for deployment!")
        
        model_pipeline = Pipeline([
            ("vectorizer", trained_vectorizer),
            ("model", trained_model)
        ])
        
        mlflow.sklearn.log_model(
            model_pipeline,
            artifact_path="artifacts",
            registered_model_name="emotion-analysis-xgboost"
        )
    else:
        print("Model did not pass validation thresholds and is not ready for deployment.")
        print(f"Details: {is_pass_thresholds['details']}")
    
    
    