import numpy as np

from Exercise.Exercise7.ExperimentFactory.EvolutionExperimentData.BudgetedEvolutionExperimentData import \
    BudgetedEvolutionExperimentData


class SalomonBudgetedEvolutionExperimentData(BudgetedEvolutionExperimentData):
    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return "Salomon"

    @property
    def lower_bound(self):
        return -100

    @property
    def upper_bound(self):
        return 100

    @property
    def known_minimum(self):
        return 0

    def evaluation_function(self, parameters):
        parameters = np.asarray(parameters)
        norm = np.sqrt(np.sum(parameters ** 2))
        return 1 - np.cos(2 * np.pi * norm) + 0.1 * norm
