from abc import ABC, abstractmethod


class Exercise(ABC):
    @abstractmethod
    def execute(self):
        pass
