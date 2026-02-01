from abc import ABC, abstractmethod
from typing import List


class ITextDataCleaning(ABC):
    @abstractmethod
    def to_lowercase(self, text: str) -> str:
        pass
    
    @abstractmethod
    def remove_punctuation(self, text: str) -> str:
        pass
    
    @abstractmethod
    def remove_stopwords(self, text: str, stopwords: List[str]) -> str:
        pass
    
    @abstractmethod
    def stem(self, text: str) -> str:
        pass
    
    @abstractmethod
    def remove_whitespace(self, text: str) -> str:
        pass
    
    @abstractmethod
    def remove_urls(self, text: str) -> str:
        pass
    
    