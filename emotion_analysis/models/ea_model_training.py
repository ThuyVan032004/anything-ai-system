import os

import boto3
import joblib
from datetime import datetime
import mlflow
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_sample_weight
from xgboost import XGBClassifier
from emotion_analysis.common.constants import AppConstants
from shared.src.data.models.s3_config_model import S3ConfigReadModel
from shared.src.data.helpers.aws_s3_helper import AwsS3Helper

from shared.src.common.env_constants import EnvConstants


if __name__ == "__main__":
    s3_bucket = os.getenv(EnvConstants.AWS_S3_BUCKET)
    access_key = os.getenv(EnvConstants.AWS_ACCESS_KEY_ID)
    secret_key = os.getenv(EnvConstants.AWS_SECRET_ACCESS_KEY)
    
    # Get train and validation data file name from SSM Parameter Store
    ssm = boto3.client(
        'ssm',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='ap-southeast-1'
    )
    
    train_file_name = ssm.get_parameter(Name="/emotion_analysis/pipeline/training_pipelines/ea_train_data")['Parameter']['Value']
    train_data = AwsS3Helper.read_data_from_s3(
        S3ConfigReadModel(
            s3_uri=f"s3://{s3_bucket}/emotion-analysis/{train_file_name}",
            access_key=access_key,
            secret_key=secret_key
        )
    )
    
    validation_file_name = ssm.get_parameter(Name="/emotion_analysis/pipeline/training_pipelines/ea_validation_data")['Parameter']['Value']
    validation_data = AwsS3Helper.read_data_from_s3(
        S3ConfigReadModel(
            s3_uri=f"s3://{s3_bucket}/emotion-analysis/{validation_file_name}",
            access_key=access_key,
            secret_key=secret_key
        )
    )
    
    # Create TF-IDF features for train and validation data
    X_train = train_data["cleaned_text"]
    y_train = train_data["label"]
    X_validation = validation_data["cleaned_text"]
    y_validation = validation_data["label"]
    
    tf = TfidfVectorizer(min_df=2,max_df=0.95,binary=False,ngram_range=(1,3), sublinear_tf=True)
    tf_train = tf.fit_transform(X_train)
    tf_validation = tf.transform(X_validation)
    
    # Compute sample weights to handle class imbalance
    sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)
    
    # Initialize and train XGBoost model
    xgb_model = XGBClassifier(
        tree_method='hist',  # GPU method
        device='cuda',           # Use 'cuda' to specify GPU
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        eval_metric='mlogloss',
        random_state=42,
        use_label_encoder=False
    )
    
    # Start mlflow run for experiment tracking
    mlflow.set_tracking_uri(AppConstants.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(AppConstants.MLFLOW_EXPERIMENT_NAME)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"xgboost_{timestamp}"
    saved_model_file_name = f"emotion_analysis_xgb_{timestamp}.joblib"
    saved_vectorizer_file_name = f"emotion_analysis_tfidf_{timestamp}.joblib"
    
    with mlflow.start_run(run_name=run_name) as run:
        # Log hyperparameters
        mlflow.log_params({
            "n_estimators": 200,
            "max_depth": 6,
            "learning_rate": 0.1,
            "eval_metric": 'mlogloss',
            "random_state": 42,
            "tfidf_min_df": 2,
            "tfidf_max_df": 0.95,
            "tfidf_ngram_range": (1, 3),
            "sublinear_tf": True
        })

        # Train model
        xgb_model.fit(
            tf_train,
            y_train,
            eval_set=[(tf_validation, y_validation)],
            verbose=10,
            sample_weight=sample_weight
        )

        # Evaluate on validation set
        y_pred = xgb_model.predict(tf_validation)
        metrics = classification_report(y_validation, y_pred, output_dict=True)

        mlflow.log_metrics({
            "accuracy": metrics["accuracy"],
            "precision_weighted": metrics["weighted avg"]["precision"],
            "recall_weighted": metrics["weighted avg"]["recall"],
            "f1_score_weighted": metrics["weighted avg"]["f1-score"]
        })

        joblib.dump(xgb_model, saved_model_file_name)
        joblib.dump(tf, saved_vectorizer_file_name)

        mlflow.log_text(classification_report(y_validation, y_pred), "classification_report.txt")
        
        client = mlflow.tracking.MlflowClient(tracking_uri=AppConstants.MLFLOW_TRACKING_URI)

        # Upload trực tiếp qua HTTP, không phụ thuộc artifact_uri
        client.log_artifact(run.info.run_id, saved_model_file_name)
        client.log_artifact(run.info.run_id, saved_vectorizer_file_name)

        # Cleanup local files
        os.remove(saved_model_file_name)
        os.remove(saved_vectorizer_file_name)

        # Lưu SSM
        ssm.put_parameter(
            Name="/emotion_analysis/mlflow/run_id",
            Value=run.info.run_id,
            Overwrite=True, Type="String"
        )
        
        ssm.put_parameter(
            Name="/emotion_analysis/mlflow/experiment_id",
            Value=run.info.experiment_id,
            Overwrite=True,
            Type="String"
        )
        
        ssm.put_parameter(
            Name="/emotion_analysis/pipeline/training_pipelines/ea_trained_model",
            Value=saved_model_file_name,
            Overwrite=True, Type="String"
        )
        ssm.put_parameter(
            Name="/emotion_analysis/pipeline/training_pipelines/ea_trained_vectorizer",
            Value=saved_vectorizer_file_name,
            Overwrite=True, Type="String"
        )