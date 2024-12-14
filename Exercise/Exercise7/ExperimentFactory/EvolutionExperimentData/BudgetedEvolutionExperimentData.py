from abc import ABC, abstractmethod

class BudgetedEvolutionExperimentData(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    def population_size(self):
        return 25

    @property
    @abstractmethod
    def lower_bound(self):
        pass

    @property
    @abstractmethod
    def upper_bound(self):
        pass

    @property
    @abstractmethod
    def known_minimum(self):
        pass

    @abstractmethod
    def evaluation_function(self, parameters):
        pass
