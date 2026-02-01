from abc import ABC
from feast import FeatureView, FileSource, KafkaSource

from shared.src.data.interfaces.i_feast import IFeast
from shared.src.data.models.feast_models import FeastFeatureViewModel, FeastFileSourceModel, FeastGetHistoricalFeaturesModel, FeastGetStreamFeaturesModel, FeastKafkaSourceModel, FeastPushToFeatureStoreModel, FeastStreamFeatureViewModel

from feast import FeatureStore

class FeastBase(IFeast, ABC):
    def __init__(self, feature_store: FeatureStore):
        self.feature_store = feature_store
        
    def create_file_source(self, properties: FeastFileSourceModel):
        return FileSource(**properties.model_dump())

    def create_kafka_source(self, properties: FeastKafkaSourceModel):
        return KafkaSource(**properties.model_dump())

    def create_feature_view(self, properties: FeastFeatureViewModel):
        return FeatureView(**properties.model_dump())    

    def get_historical_features(self, properties: FeastGetHistoricalFeaturesModel):
        return self.feature_store.get_historical_features(
            **properties.model_dump()
        )

    def get_online_features(self, properties: FeastGetStreamFeaturesModel):
        return self.feature_store.get_online_features(
            **properties.model_dump()
        )

    def push_feature_to_store(self, properties: FeastPushToFeatureStoreModel):
        return self.feature_store.push(
            **properties.model_dump()
        )