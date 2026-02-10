from typing import List
from src.data.corpus_profiling_base import CorpusProfilingBase


class EMCorpusProfiling(CorpusProfilingBase):
    def __init__(self, configs: List[str]):
        super().__init__(configs)
        
if __name__ == "__main__":
    pass