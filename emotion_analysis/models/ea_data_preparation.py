from datetime import datetime
import os

import boto3
from shared.src.models.models.tabular_data_preparation_config_model import TabularDataPreparationConfigModel
from shared.src.data.helpers.aws_s3_helper import AwsS3Helper
from shared.src.data.models.s3_config_model import S3ClientConfigModel, S3ConfigReadModel, S3ConfigWriteFileModel

from shared.src.common.env_constants import EnvConstants
from shared.src.models.tabular_data_preparation_base import TabularDataPreparationBase


class TabularDataPreparation(TabularDataPreparationBase):
    def __init__(self, data_frame):
        super().__init__(data_frame)


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
    file_name = ssm.get_parameter(Name="/emotion_analysis/pipeline/data_pipelines/data_cleaned")['Parameter']['Value']
    
    data_frame = AwsS3Helper.read_data_from_s3(
        S3ConfigReadModel(
            s3_uri=f"s3://{s3_bucket}/emotion-analysis/{file_name}",
            access_key=access_key,
            secret_key=secret_key
        )
    )
    
    # Split data into train, validation and test sets
    data_preparer = TabularDataPreparation(data_frame)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    data_preparer.prepare_data(
        configs=TabularDataPreparationConfigModel(
            saved_training_file_name=f"ea_train_data_{timestamp}.parquet",
            saved_validation_file_name=f"ea_validation_data_{timestamp}.parquet",
            saved_test_file_name=f"ea_test_data_{timestamp}.parquet"
        )
    )
    
    # Save path into SSM Parameter Store
    ssm = boto3.client(
        'ssm',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='ap-southeast-1'
    )
    
    for key in ["ea_train_data", "ea_validation_data", "ea_test_data"]:
        file_name = f"{key}_{timestamp}.parquet"
        ssm.put_parameter(
            Name=f"/emotion_analysis/pipeline/training_pipelines/{key}",
            Value=file_name,
            Overwrite=True,
            Type="String"
        )
        
        AwsS3Helper.upload_file_to_s3(
            S3ClientConfigModel(
                access_key=access_key,
                secret_key=secret_key
            ),
            S3ConfigWriteFileModel(
                file_name=file_name,
                s3_bucket_name=s3_bucket,
                s3_file_path=f"emotion-analysis/{file_name}"
            )
        )
    
    print("Data preparation for emotion analysis completed successfully.")
    