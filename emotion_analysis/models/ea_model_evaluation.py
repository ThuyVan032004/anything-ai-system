import json
import os

import boto3
import joblib
import mlflow
from sklearn.metrics import classification_report
from emotion_analysis.common.constants import AppConstants
from shared.src.data.models.s3_config_model import S3ConfigReadModel
from shared.src.data.helpers.aws_s3_helper import AwsS3Helper

from shared.src.common.env_constants import EnvConstants


if __name__ == "__main__":
    s3_bucket = os.getenv(EnvConstants.AWS_S3_BUCKET)
    access_key = os.getenv(EnvConstants.AWS_ACCESS_KEY_ID)
    secret_key = os.getenv(EnvConstants.AWS_SECRET_ACCESS_KEY)
    
    ssm = boto3.client(
        'ssm',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='ap-southeast-1'
    )
    
    # Get vectorizer file name from SSM Parameter Store
    vectorizer_file_name = ssm.get_parameter(Name="/emotion_analysis/pipeline/training_pipelines/ea_trained_vectorizer")['Parameter']['Value']
    
    # Get trained model and vectorizer model
    run_id = ssm.get_parameter(Name="/emotion_analysis/mlflow/run_id")['Parameter']['Value']
    experiment_id = ssm.get_parameter(Name="/emotion_analysis/mlflow/experiment_id")['Parameter']['Value']
    model_file_name = ssm.get_parameter(Name="/emotion_analysis/pipeline/training_pipelines/ea_trained_model")['Parameter']['Value']
    vectorizer_file_name = ssm.get_parameter(Name="/emotion_analysis/pipeline/training_pipelines/ea_trained_vectorizer")['Parameter']['Value']
    
    print(f"[DEBUG] run_id: {run_id}")
    print(f"[DEBUG] experiment_id: {experiment_id}")
    print(f"[DEBUG] model_file_name: {model_file_name}")
    print(f"[DEBUG] vectorizer_file_name: {vectorizer_file_name}")
    

    mlflow.set_tracking_uri(AppConstants.MLFLOW_TRACKING_URI)

    # ✅ Download qua HTTP proxy — không dùng models:/ hay runs:/ URI
    model_path = mlflow.artifacts.download_artifacts(
        f"mlflow-artifacts:/{experiment_id}/{run_id}/artifacts/{model_file_name}",
    )
    vectorizer_path = mlflow.artifacts.download_artifacts(
        artifact_uri=f"mlflow-artifacts:/{experiment_id}/{run_id}/artifacts/{vectorizer_file_name}",
    )

    print(f"[DEBUG] model_path: {model_path}")
    print(f"[DEBUG] vectorizer_path: {vectorizer_path}")

    trained_model = joblib.load(model_path)
    trained_vectorizer = joblib.load(vectorizer_path)
    
    test_file_name = ssm.get_parameter(Name="/emotion_analysis/pipeline/training_pipelines/ea_test_data")['Parameter']['Value']
    test_data = AwsS3Helper.read_data_from_s3(
        S3ConfigReadModel(
            s3_uri=f"s3://{s3_bucket}/emotion-analysis/{test_file_name}",
            access_key=access_key,
            secret_key=secret_key
        )
    )
    
    X_test = test_data["cleaned_text"]
    y_test = test_data["label"]
    
    tf_test = trained_vectorizer.transform(X_test)
    
    predictions = trained_model.predict(tf_test)
    report = classification_report(y_test, predictions, output_dict=True)
    
    ssm.put_parameter(
        Name="/emotion_analysis/pipeline/training_pipelines/ea_test_evaluation_report",
        Value=json.dumps(report),
        Overwrite=True,
        Type="String"
    )