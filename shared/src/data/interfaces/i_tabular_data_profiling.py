from abc import ABC, abstractmethod
from typing import Dict

import pandas as pd

class ITabularDataProfiling(ABC):
    @abstractmethod
    def get_data_schema(self) -> Dict[str, str]:
        pass
    
    @abstractmethod
    def get_statistics(self) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def get_missing_values_summary(self) -> Dict[str, int]:
        pass
    
    