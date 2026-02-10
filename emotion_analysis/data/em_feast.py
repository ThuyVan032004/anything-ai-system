from feast import FeatureStore
from src.data.feast_base import FeastBase


class EMFeast(FeastBase):
    def __init__(self, feature_store: FeatureStore):
        super().__init__(feature_store)