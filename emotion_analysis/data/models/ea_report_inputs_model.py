from typing import Dict, Optional
import pandas as pd
from pydantic import BaseModel
from src.data.models.corpus_profiling_models import LengthProfileModel, RedundancyProfileModel, VocabularyProfileModel


class EAReportInputsModel(BaseModel):
    data_schema: Dict[str, str]
    statistics: Optional[pd.DataFrame] = None   
    missing_values_summary: Dict[str, int]
    vocabulary_profile: VocabularyProfileModel
    length_profile: LengthProfileModel
    redundancy_profile: RedundancyProfileModel