import numpy as np

from Exercise.Exercise7.ExperimentFactory.EvolutionExperimentData.BudgetedEvolutionExperimentData import \
    BudgetedEvolutionExperimentData


class RosenbrockBudgetedEvolutionExperimentData(BudgetedEvolutionExperimentData):
    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return "Generalized Rosenbrock"

    @property
    def lower_bound(self):
        return -30

    @property
    def upper_bound(self):
        return 30

    @property
    def known_minimum(self):
        return 0

    def evaluation_function(self, parameters):
        parameters = np.asarray(parameters)
        xi = parameters[:-1]
        xi1 = parameters[1:]
        return np.sum(100 * (xi1 - xi ** 2) ** 2 + (xi - 1) ** 2)