import numpy as np

from Exercise.Exercise7.ExperimentFactory.EvolutionExperimentData.BudgetedEvolutionExperimentData import \
    BudgetedEvolutionExperimentData


class WhitleyBudgetedEvolutionExperimentData(BudgetedEvolutionExperimentData):
    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return "Whitley"

    @property
    def lower_bound(self):
        return -10.24

    @property
    def upper_bound(self):
        return 10.24

    @property
    def known_minimum(self):
        return 0

    def evaluation_function(self, parameters):
        parameters = np.asarray(parameters)

        # Create pairwise combinations for all k and j
        x_k, x_j = np.meshgrid(parameters, parameters, indexing='ij')  # x_k corresponds to k, x_j corresponds to j

        # Compute y_{j,k} for all pairs
        y_jk = 100 * (x_k - x_j ** 2) ** 2 + (1 - x_j) ** 2

        # Apply the formula
        result = np.sum((y_jk ** 2 / 4000) - np.cos(y_jk) + 1)
        return result