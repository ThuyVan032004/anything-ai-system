from src.data.models.tabular_data_cleaning_models import TabularMissingValueProps, TabularOutlierProps
from shared.src.data.helpers.tabular_data_helper import TabularDataCleaningHelper
from shared.src.data.interfaces.i_tabular_data_cleaning import ITabularDataCleaning

import pandas as pd

class TabularDataCleaningBase(ITabularDataCleaning):
    def __init__(self, data_frame: pd.DataFrame):
        self.data_frame = data_frame
        
    def handle_missing_values(self, properties: TabularMissingValueProps):
        column = properties.column
        
        if properties.method == "mean":
            self.data_frame[column] = self.data_frame[column].fillna(self.data_frame[column].mean())
        elif properties.method == "median":
            self.data_frame[column] = self.data_frame[column].fillna(self.data_frame[column].median())
        elif properties.method == "mode":
            self.data_frame[column] = self.data_frame[column].fillna(self.data_frame[column].mode()[0])
        elif properties.method == "drop":
            self.data_frame.dropna(subset=[column], inplace=True)
        elif properties.method == "constant":
            self.data_frame[column] = self.data_frame[column].fillna(properties.fill_value)
        
        return self.data_frame
    
    def remove_duplicates(self):
        self.data_frame = self.data_frame.drop_duplicates()
        return self.data_frame
    
    def handle_outliers(self, properties: TabularOutlierProps):
        """Handle outliers using IQR"""
        lower_bound, upper_bound = TabularDataCleaningHelper.calculate_iqr_bounds(self.data_frame[properties.column])
        
        if properties.method == "remove":
            self.data_frame = self.data_frame[
                (self.data_frame[properties.column] >= lower_bound) & 
                (self.data_frame[properties.column] <= upper_bound)
            ]
        elif properties.method == "cap":
            self.data_frame.loc[self.data_frame[properties.column] < lower_bound, properties.column] = lower_bound
            self.data_frame.loc[self.data_frame[properties.column] > upper_bound, properties.column] = upper_bound
            
        return self.data_frame
    
    def remove_columns(self, columns: list[str]) -> pd.DataFrame:
        self.data_frame = self.data_frame.drop(columns=columns)
        return self.data_frame
    
    def normalize(self, column: str) -> pd.DataFrame:
        """Normalize data using Min-Max scaling."""
        self.data_frame[column] = TabularDataCleaningHelper.calculate_min_max_normalization(self.data_frame[column])
        return self.data_frame
    
    def standardize(self, column: str) -> pd.DataFrame:
        """Standardize data using Z-score standardization."""
        self.data_frame[column] = TabularDataCleaningHelper.calculate_z_score_standardization(self.data_frame[column])
        return self.data_frame