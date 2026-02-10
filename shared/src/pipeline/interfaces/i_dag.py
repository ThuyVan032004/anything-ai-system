from abc import ABC, abstractmethod


class IDag(ABC):
    @abstractmethod
    def build(self):
        pass
    
    @abstractmethod
    def create_docker_task(self):
        pass