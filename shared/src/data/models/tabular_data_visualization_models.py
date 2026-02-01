from pandas import Series
from pydantic import BaseModel


class TabularPlotDistributionModel(BaseModel):
    series: Series
    plot_title: str
    