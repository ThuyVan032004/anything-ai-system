from pydantic import BaseModel


class S3ConfigReadModel(BaseModel):
    s3_uri: str
    access_key: str
    secret_key: str
    
class S3ConfigWriteFileModel(BaseModel):
    file_name: str
    s3_bucket_name: str
    s3_file_path: str
    
class S3ClientConfigModel(BaseModel):
    access_key: str
    secret_key: str