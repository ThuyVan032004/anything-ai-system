import pandas as pd


class TabularDataCleaningHelper:
    @staticmethod
    def calculate_iqr_bounds(series: pd.Series) -> tuple[float, float]:
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        return lower_bound, upper_bound
    
    @staticmethod
    def calculate_min_max_normalization(series: pd.Series) -> pd.Series:
        min_val = series.min()
        max_val = series.max()
        return (series - min_val) / (max_val - min_val)
    
    @staticmethod
    def calculate_z_score_standardization(series: pd.Series) -> pd.Series:
        mean = series.mean()
        std = series.std()
        return (series - mean) / std