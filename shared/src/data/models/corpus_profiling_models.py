from typing import Dict, List, Tuple

from pydantic import BaseModel


class VocabularyProfileModel(BaseModel):
    total_words: int
    unique_words: int
    top_words: List[Tuple[str, int]]  # List of (word, count) tuples
    
class LengthProfileModel(BaseModel):
    mean_length: float
    median_length: float
    standard_deviation: float
    max_length: int
    min_length: int
    
class RedundancyProfileModel(BaseModel):
    unique_rows: int
    total_rows: int
    redundancy_ratio: float