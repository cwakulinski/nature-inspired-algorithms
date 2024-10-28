from abc import ABC, abstractmethod


class SimulatedAnnealingExperimentData(ABC):
    @property
    def starting_point(self):
        return [self.upper_bound] * self.dimensions

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def dimensions(self):
        pass

    @property
    @abstractmethod
    def lower_bound(self):
        pass

    @property
    @abstractmethod
    def upper_bound(self):
        pass

    @abstractmethod
    def evaluation_function(self, parameters):
        pass
