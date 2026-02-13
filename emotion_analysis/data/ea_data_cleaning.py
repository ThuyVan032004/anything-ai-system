import nltk
import pandas as pd
from dotenv import load_dotenv
import os
from src.common.env_constants import EnvConstants
from src.data.helpers.aws_s3_helper import AwsS3Helper
from src.data.models.s3_config_model import S3ClientConfigModel, S3ConfigReadModel, S3ConfigWriteFileModel
from src.data.models.tabular_data_cleaning_models import TabularMissingValueProps
from src.data.tabular_data_cleaning_base import TabularDataCleaningBase
from src.data.text_data_cleaning_base import TextDataCleaningBase

from emotion_analysis.data.helpers.text_data_cleaning_helper import TextDataCleaningHelper

# Load environment variables from .env file
load_dotenv()

nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


class EATabularDataCleaning(TabularDataCleaningBase):
    def __init__(self, data_frame: pd.DataFrame):
        super().__init__(data_frame)
        
class EATextDataCleaning(TextDataCleaningBase):
    def __init__(self):
        super().__init__()
        
        
        
if __name__ == "__main__":
    s3_bucket = os.getenv(EnvConstants.AWS_S3_BUCKET)
    access_key = os.getenv(EnvConstants.AWS_ACCESS_KEY_ID)
    secret_key = os.getenv(EnvConstants.AWS_SECRET_ACCESS_KEY)
    
    s3_uri = f"s3://{s3_bucket}/emotion-analysis/data.csv"
    
    data_frame = AwsS3Helper.read_data_from_s3(
        S3ConfigReadModel(
            s3_uri=s3_uri,
            access_key=access_key,
            secret_key=secret_key
        )
    )
    
    
    ea_tabular_data_cleaner = EATabularDataCleaning(data_frame)
    
    # Drop column Unnamed: 0 if exists
    if "Unnamed: 0" in data_frame.columns:
        data_frame = ea_tabular_data_cleaner.remove_columns(["Unnamed: 0"])
        
    data_frame = ea_tabular_data_cleaner.remove_duplicates()
    
    for column in data_frame.columns:
        if data_frame[column].isnull().sum() > 0:
            data_frame = ea_tabular_data_cleaner.handle_missing_values(
                TabularMissingValueProps(
                    column=column,
                    method="drop"
                )
            )
    
    ea_text_data_cleaner = EATextDataCleaning()
    
    data_frame["text"] = data_frame["text"].apply(
        TextDataCleaningHelper.clean_text
    )
    
    data_frame = data_frame.rename(columns={"text": "cleaned_text"})
    
    data_frame.to_parquet("20260211_data_processed_v1.0.parquet", index=False)
    
    AwsS3Helper.upload_file_to_s3(
        S3ClientConfigModel(
            access_key=access_key,
            secret_key=secret_key
        ),
        S3ConfigWriteFileModel(
            file_name="20260211_data_processed_v1.0.parquet",
            s3_bucket_name=s3_bucket,
            s3_file_path="emotion-analysis/20260211_data_processed_v1.0.parquet"
        )
    )
    
    
    
    
    
    
    
    
    
    
    