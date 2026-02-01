from typing import Dict
import pandas as pd
from shared.src.data.interfaces.i_tabular_data_profiling import ITabularDataProfiling


class TabularDataProfilingBase(ITabularDataProfiling):
    def __init__(self, data_frame: pd.DataFrame):
        self.data_frame = data_frame
        
    def get_data_schema(self) -> Dict[str, str]:
        return self.data_frame.dtypes.apply(lambda x: x.name).to_dict()

    def get_statistics(self) -> pd.DataFrame:
        return self.data_frame.describe()
    
    def get_missing_values_summary(self) -> Dict[str, int]:
        return self.data_frame.isnull().sum().to_dict()