from typing import List
import pandas as pd
from src.data.corpus_visualization_base import CorpusVisualizationBase
from src.data.tabular_data_visualization_base import TabularDataVisualizationBase


class EATabularDataVisualization(TabularDataVisualizationBase):
    def __init__(self, data_frame: pd.DataFrame):
        super().__init__(data_frame)
        
class EACorpusVisualization(CorpusVisualizationBase):
    def __init__(self, configs: List[str]):
        super().__init__(configs)
        
        
if __name__ == "__main__":
    pass