from abc import ABC, abstractmethod


class IDag(ABC):
    @abstractmethod
    def build(self):
        pass