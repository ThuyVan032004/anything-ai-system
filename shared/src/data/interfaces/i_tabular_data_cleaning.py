from abc import ABC, abstractmethod
import pandas as pd

from src.data.models.tabular_data_cleaning_models import TabularMissingValueProps, TabularOutlierProps

class ITabularDataCleaning(ABC):
    @abstractmethod
    def handle_missing_values(self, properties: TabularMissingValueProps) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def remove_duplicates(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def handle_outliers(self, properties: TabularOutlierProps) -> pd.DataFrame:
        """Handle outliers using IQR"""
        pass

    @abstractmethod
    def remove_columns(self, columns: list[str]) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def normalize(self) -> pd.DataFrame:
        """Normalize data using Min-Max scaling."""
        pass
    
    @abstractmethod
    def standardize(self) -> pd.DataFrame:
        """Standardize data using Z-score standardization."""
        pass
    