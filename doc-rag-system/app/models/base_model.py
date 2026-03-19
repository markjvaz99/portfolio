from abc import ABC, abstractmethod

class BaseModelProvider(ABC):

    @abstractmethod
    def chat(self, messages, **kwargs):
        pass