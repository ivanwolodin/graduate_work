from abc import ABC, abstractmethod


class BaseProducer(ABC):

    @abstractmethod
    def produce(self, *args, **kwargs):
        pass
