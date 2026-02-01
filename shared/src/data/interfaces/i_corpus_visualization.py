from abc import ABC, abstractmethod
from typing import List


class ICorpusVisualization(ABC):
    @abstractmethod
    def plot_frequency_distribution(self) -> None:
        pass
    
    @abstractmethod
    def generate_word_cloud(self) -> None:
        pass