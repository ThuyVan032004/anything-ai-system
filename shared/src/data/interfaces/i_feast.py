from abc import ABC, abstractmethod


class IFeast(ABC):
    @abstractmethod
    def create_file_source(self):
        pass
    
    @abstractmethod
    def create_kafka_source(self):
        pass
    
    @abstractmethod
    def create_feature_view(self):
        pass
    
    @abstractmethod
    def get_historical_features(self):
        pass
    
    @abstractmethod
    def get_online_features(self):
        pass   
    
    @abstractmethod
    def push_feature_to_offline_store(self):
        pass
    
    @abstractmethod
    def push_feature_to_online_store(self):
        pass