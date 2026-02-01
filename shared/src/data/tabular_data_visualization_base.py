from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
from shared.src.data.interfaces.i_tabular_data_visualization import ITabularDataVisualization
from shared.src.data.models.tabular_data_visualization_models import TabularPlotDistributionModel


class TabularDataVisualizationBase(ITabularDataVisualization):
    def __init__(self, data_frame: pd.DataFrame):
        self.data_frame = data_frame
        
    def plot_distribution(self, properties: TabularPlotDistributionModel):
        plt.figure(figsize=(10, 6))
        sns.histplot(properties.series, kde=True)
        plt.title(f'Distribution of {properties.plot_title}')
        plt.show()
        
    def plot_correlation_matrix(self):
        plt.figure(figsize=(12, 8))
        correlation_matrix = self.data_frame.select_dtypes(include=['number']).corr()
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.show()