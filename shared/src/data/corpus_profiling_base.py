from abc import ABC
from collections import Counter
from typing import List
import numpy as np
from src.data.interfaces.i_corpus_profiling import ICorpusProfiling
from src.data.models.corpus_profiling_models import LengthProfileModel, RedundancyProfileModel, VocabularyProfileModel


class CorpusProfilingBase(ICorpusProfiling, ABC):
    def __init__(self, corpus: List[str]):
        self.corpus = corpus
        
    def profile_vocabulary(self) -> VocabularyProfileModel:
        words = []
        for text in self.corpus:
            words.extend(text.lower().split())
        
        word_counts = Counter(words)
        
        total_words = len(words)
        unique_words = len(set(words))
        top_words = word_counts.most_common(10)
        
        return VocabularyProfileModel(
            total_words=total_words, 
            unique_words=unique_words, 
            top_words=top_words
        )
    
    def profile_length(self) -> LengthProfileModel:
        lengths = [len(text.split()) for text in self.corpus]
        
        return LengthProfileModel(
            mean_length=sum(lengths) / len(lengths) if lengths else 0,
            max_length=max(lengths) if lengths else 0,
            min_length=min(lengths) if lengths else 0,
            median_length=sorted(lengths)[len(lengths)//2] if lengths else 0,
            standard_deviation=np.std(lengths) if lengths else 0
        )
    
    def profile_redundancy(self) -> RedundancyProfileModel:
        total_rows = len(self.corpus)
        unique_rows = len(set(self.corpus))
        redundancy_ratio = (total_rows - unique_rows) / total_rows if total_rows > 0 else 0
        
        return RedundancyProfileModel(
            unique_rows=unique_rows,
            total_rows=total_rows,
            redundancy_ratio=redundancy_ratio
        )