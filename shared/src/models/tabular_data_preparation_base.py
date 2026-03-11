from abc import ABC
import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from shared.src.data.models.s3_config_model import S3ClientConfigModel, S3ConfigWriteFileModel
from shared.src.data.helpers.aws_s3_helper import AwsS3Helper
from shared.src.models.models.tabular_data_preparation_config_model import TabularDataPreparationConfigModel
from shared.src.models.interfaces.i_data_preparation import IDataPreparation


class TabularDataPreparationBase(IDataPreparation, ABC):
    def __init__(self, data_frame: pd.DataFrame):
        self.data_frame = data_frame
    
    def prepare_data(self, configs: TabularDataPreparationConfigModel):
        saved_training_file_name = configs.saved_training_file_name
        saved_validation_file_name = configs.saved_validation_file_name
        saved_test_file_name = configs.saved_test_file_name
        split_ratios = configs.split_ratios
        
        train_df, temp_df = train_test_split(
            self.data_frame,
            test_size=split_ratios["validation_and_test"],
            stratify=self.data_frame["label"],
            random_state=42
        )
        
        validation_df, test_df = train_test_split(
            temp_df,
            test_size=split_ratios["test"],
            stratify=temp_df["label"],
            random_state=42
        )

        train_df.to_parquet(saved_training_file_name, index=False)
        validation_df.to_parquet(saved_validation_file_name, index=False)
        test_df.to_parquet(saved_test_file_name, index=False)
        