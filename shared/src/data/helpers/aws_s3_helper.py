import pandas as pd
from src.data.models.s3_config_model import S3ClientConfigModel, S3ConfigReadModel, S3ConfigWriteFileModel


class AwsS3Helper:
    @staticmethod
    def read_data_from_s3(s3_configs: S3ConfigReadModel) -> pd.DataFrame:
        s3_uri = s3_configs.s3_uri
        s3_access_key = s3_configs.access_key
        s3_secret_key = s3_configs.secret_key
        
        uri_extension = s3_uri.split('.')[-1]
        
        if uri_extension == "csv":
            return pd.read_csv(
                s3_uri,
                storage_options={
                    "key": s3_access_key,
                    "secret": s3_secret_key,
                    "client_kwargs": {"region_name": "ap-southeast-1"}
                }
            )
        
        if uri_extension == "parquet":
            return pd.read_parquet(
                s3_uri,
                storage_options={
                    "key": s3_access_key,
                    "secret": s3_secret_key,
                    "client_kwargs": {"region_name": "ap-southeast-1"}
                }
            )
            
        raise ValueError(f"Unsupported file extension: {uri_extension}")
    
    @staticmethod
    def upload_file_to_s3(s3_client_config: S3ClientConfigModel, s3_upload_file_config: S3ConfigWriteFileModel) -> None:
        import boto3

        s3 = boto3.client(
            's3',
            aws_access_key_id=s3_client_config.access_key,
            aws_secret_access_key=s3_client_config.secret_key,
            region_name = "ap-southeast-1"
        )

        try:
            s3.upload_file(
                s3_upload_file_config.file_name,
                s3_upload_file_config.s3_bucket_name,
                s3_upload_file_config.s3_file_path
            )
            
            print("Upload Successful")
        except FileNotFoundError:
            print("The file was not found")
        # except NoCredentialsError:
        #     print("Credentials not available")
        # except ClientError as e:
        #     print(f"Client error: {e}")
        