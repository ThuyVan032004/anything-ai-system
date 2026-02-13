import datetime
import os
from dotenv import load_dotenv
from typing import List
import pandas as pd
from src.common.env_constants import EnvConstants
from src.data.corpus_profiling_base import CorpusProfilingBase
from src.data.helpers.aws_s3_helper import AwsS3Helper
from src.data.models.s3_config_model import S3ClientConfigModel, S3ConfigReadModel, S3ConfigWriteFileModel
from src.data.tabular_data_profiling_base import TabularDataProfilingBase

from emotion_analysis.common.constants import AppConstants
from emotion_analysis.data.helpers.ea_profiling_helper import EAProfilingHelper
from emotion_analysis.data.models.ea_report_inputs_model import EAReportInputsModel

load_dotenv()


class EATabularDataProfiling(TabularDataProfilingBase):
    def __init__(self, data_frame: pd.DataFrame):
        super().__init__(data_frame)
        
class EACorpusProfiling(CorpusProfilingBase):
    def __init__(self, configs: List[str]):
        super().__init__(configs)
        
if __name__ == "__main__":
    s3_bucket = os.getenv(EnvConstants.AWS_S3_BUCKET)
    access_key = os.getenv(EnvConstants.AWS_ACCESS_KEY_ID)
    secret_key = os.getenv(EnvConstants.AWS_SECRET_ACCESS_KEY)
    
    data_frame = AwsS3Helper.read_data_from_s3(
        S3ConfigReadModel(
            s3_uri=f"s3://{s3_bucket}/emotion-analysis/{AppConstants.PROCESSED_FILE_NAME}",
            access_key=access_key,
            secret_key=secret_key
        )
    )
    
    ea_tabular_data_profiler = EATabularDataProfiling(data_frame)
    
    data_schema = ea_tabular_data_profiler.get_data_schema()
    missing_values_summary = ea_tabular_data_profiler.get_missing_values_summary()
    
    corpus = data_frame["cleaned_text"].tolist()
    ea_corpus_profiler = EACorpusProfiling(corpus)
    
    vocabulary_profile = ea_corpus_profiler.profile_vocabulary()
    length_profile = ea_corpus_profiler.profile_length()
    redundancy_profile = ea_corpus_profiler.profile_redundancy()
    
    data_validation_result = EAProfilingHelper.validate_data(EAReportInputsModel(
        data_schema=data_schema,
        missing_values_summary=missing_values_summary,
        vocabulary_profile=vocabulary_profile,
        length_profile=length_profile,
        redundancy_profile=redundancy_profile
    ))
    
    output_file = EAProfilingHelper.generate_report(data_validation_result)
    
    AwsS3Helper.upload_file_to_s3(
        S3ClientConfigModel(
            access_key=access_key,
            secret_key=secret_key,
        ),
        S3ConfigWriteFileModel(
            file_name=output_file,
            s3_bucket_name=s3_bucket,
            s3_file_path=f"emotion-analysis/{os.path.basename(output_file)}"
        )
    )
    
    

    
    
    
    
    
    
    
    
    
    
    
    