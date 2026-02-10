import pandas as pd
from src.data.tabular_data_cleaning_base import TabularDataCleaningBase


class EMTabularDataCleaning(TabularDataCleaningBase):
    def __init__(self, data_frame: pd.DataFrame):
        super().__init__(data_frame)
        
if __name__ == "__main__":
    pass