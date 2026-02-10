from typing import List
from src.data.corpus_visualization_base import CorpusVisualizationBase


class EMCorpusVisualization(CorpusVisualizationBase):
    def __init__(self, configs: List[str]):
        super().__init__(configs)
        
if __name__ == "__main__":
    pass