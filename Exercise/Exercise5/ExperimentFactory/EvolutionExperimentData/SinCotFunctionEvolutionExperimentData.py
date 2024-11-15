import math

from Exercise.Exercise5.ExperimentFactory.EvolutionExperimentData.EvolutionExperimentData import EvolutionExperimentData


class SinCotFunctionEvolutionExperimentData(EvolutionExperimentData):

    @property
    def name(self):
        return "sin_cot_function"

    @property
    def dimensions(self):
        return 10

    @property
    def population_size(self):
        return 10

    @property
    def lower_bound(self):
        return -3

    @property
    def upper_bound(self):
        return 3

    def evaluation_function(self, parameters):
        numerator = -5
        denominator = 1 + sum(x ** 2 for x in parameters)
        fraction = numerator / denominator

        if abs(fraction) > 700:
            fraction = math.copysign(700, fraction)

        return fraction + math.sin(SinCotFunctionEvolutionExperimentData._cot(math.exp(fraction)))

    @staticmethod
    def _cot(x):
        epsilon = 1e-10
        return 1 / (math.tan(x) + epsilon)
