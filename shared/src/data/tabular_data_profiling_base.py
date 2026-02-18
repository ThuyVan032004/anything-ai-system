from typing import Dict
import pandas as pd
from src.data.interfaces.i_tabular_data_profiling import ITabularDataProfiling


class TabularDataProfilingBase(ITabularDataProfiling):
    def __init__(self, data_frame: pd.DataFrame):
        self.data_frame = data_frame
        
    def get_data_schema(self) -> Dict[str, str]:
        return self.data_frame.dtypes.apply(lambda x: x.name).to_dict()

    def get_statistics(self) -> pd.DataFrame:
        return self.data_frame.describe()
    
    def get_missing_values_summary(self):
        total_missing_values = self.data_frame.isnull().sum().to_dict()
        total_rows = len(self.data_frame)
        
        missing_values_summary = {}
        
        for key, value in total_missing_values.items():
            missing_values_summary[key] = {
                "missing_count": value,
                "missing_percentage": (value / total_rows)
            }
        
        return missing_values_summary