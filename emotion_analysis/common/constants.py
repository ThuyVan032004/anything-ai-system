from datetime import datetime

class AppConstants:
    INPUT_RAW_FILE_NAME = "data.csv"
    DATA_PIPELINE_DOCKER_IMAGE = "emotion_analysis/data_pipelines"
    TRAINING_PIPELINE_DOCKER_IMAGE = "emotion_analysis/training_pipelines"
    MLFLOW_TRACKING_URI = "http://mlflow:5000"
    MLFLOW_EXPERIMENT_NAME = "emotion-analysis_xgboost"
    MODEL_VALIDATION_THRESHOLDS = {
        "accuracy": 0.5,
        "precision_weighted": 0.5,
        "recall_weighted": 0.5,
        "f1_score_weighted": 0.5
    }