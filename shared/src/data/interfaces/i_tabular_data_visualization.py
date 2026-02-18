from abc import ABC, abstractmethod

import pandas as pd

from src.data.models.tabular_data_visualization_models import TabularPlotDistributionModel


class ITabularDataVisualization(ABC):
    @abstractmethod
    def plot_distribution(self, properties: TabularPlotDistributionModel) -> None:
        pass

    @abstractmethod
    def plot_correlation_matrix(self) -> None:
        pass