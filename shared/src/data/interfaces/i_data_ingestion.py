from abc import ABC, abstractmethod

import pandas as pd


class IDataIngestion(ABC):
    @abstractmethod
    def ingest_data(self) -> pd.DataFrame:
        pass