from abc import ABC, abstractmethod

from src.data.models.corpus_profiling_models import RedundancyProfileModel, LengthProfileModel, VocabularyProfileModel


class ICorpusProfiling(ABC):
    @abstractmethod
    def profile_vocabulary(self) -> VocabularyProfileModel:
        pass
    
    @abstractmethod
    def profile_length(self) -> LengthProfileModel:
        pass
    
    @abstractmethod
    def profile_redundancy(self) -> RedundancyProfileModel:
        pass
    
    