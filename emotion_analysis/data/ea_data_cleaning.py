import os
import boto3
import nltk
import pandas as pd
from datetime import datetime
from shared.src.common.env_constants import EnvConstants
from shared.src.data.helpers.aws_s3_helper import AwsS3Helper
from shared.src.data.models.s3_config_model import S3ClientConfigModel, S3ConfigReadModel, S3ConfigWriteFileModel
from shared.src.data.models.tabular_data_cleaning_models import TabularMissingValueProps
from shared.src.data.tabular_data_cleaning_base import TabularDataCleaningBase
from shared.src.data.text_data_cleaning_base import TextDataCleaningBase

from emotion_analysis.data.helpers.text_data_cleaning_helper import TextDataCleaningHelper

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
    
    # --- Bước 1: Tabular cleaning ban đầu ---
    ea_tabular_data_cleaner = EATabularDataCleaning(data_frame)
    
    if "Unnamed: 0" in data_frame.columns:
        data_frame = ea_tabular_data_cleaner.remove_columns(["Unnamed: 0"])
        
    data_frame = ea_tabular_data_cleaner.remove_duplicates()

    # --- Bước 2: Filter length + Text cleaning ---
    data_frame = data_frame[
        data_frame["text"].apply(lambda x: 3 <= len(x.split()) <= 100)
    ].copy()
    
    data_frame["text"] = data_frame["text"].apply(TextDataCleaningHelper.clean_text)
    
    # DEBUG: kiểm tra data sau cleaning
    print(f"Rows after cleaning: {len(data_frame)}")
    print(f"Sample cleaned texts:")
    print(data_frame["text"].head(10).tolist())
    print(f"Empty texts: {(data_frame['text'].str.strip() == '').sum()}")
    print(f"Label distribution:\n{data_frame['label'].value_counts()}")

    # --- Bước 3: Đổi tên cột và export ---
    data_frame = data_frame.rename(columns={"text": "cleaned_text"})
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    cleaned_file = f"data_cleaned_{timestamp}.parquet"
    data_frame.to_parquet(cleaned_file, index=False)
    
    # Save path into SSM Parameter Store
    ssm = boto3.client(
        'ssm',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='ap-southeast-1'
    )
    ssm.put_parameter(
        Name="/emotion_analysis/pipeline/data_pipelines/data_cleaned",
        Value=cleaned_file,
        Overwrite=True,
        Type="String"
    )
    
    AwsS3Helper.upload_file_to_s3(
        S3ClientConfigModel(
            access_key=access_key,
            secret_key=secret_key
        ),
        S3ConfigWriteFileModel(
            file_name=cleaned_file,
            s3_bucket_name=s3_bucket,
            s3_file_path=f"emotion-analysis/{cleaned_file}"
        )
    )