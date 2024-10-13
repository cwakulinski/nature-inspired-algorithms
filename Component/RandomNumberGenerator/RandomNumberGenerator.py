from abc import ABC, abstractmethod


class RandomNumberGenerator(ABC):
    @abstractmethod
    def generate(self):
        pass
