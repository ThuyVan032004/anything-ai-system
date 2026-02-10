import pandas as pd
from src.data.tabular_data_visualization_base import TabularDataVisualizationBase


class EMTabularDataVisualization(TabularDataVisualizationBase):
    def __init__(self, data_frame: pd.DataFrame):
        super().__init__(data_frame)
        
if __name__ == "__main__":
    pass