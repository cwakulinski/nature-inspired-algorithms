import math

from Exercise.Exercise4.ExperimentFactory.SimulatedAnnealingExperimentData.SimulatedAnnealingExperimentData import \
    SimulatedAnnealingExperimentData


class SimulatedAnnealingTrigonometricExperimentData(SimulatedAnnealingExperimentData):
    @property
    def name(self):
        return "trigonometric"

    @property
    def dimensions(self):
        return 10

    @property
    def lower_bound(self):
        return -3

    @property
    def upper_bound(self):
        return 3

    def evaluation_function(self, parameters):
        numerator = -5
        denominator = 1 +sum(x ** 2 for x in parameters)
        fraction = numerator / denominator

        if abs(fraction) > 700:
            fraction = math.copysign(700, fraction)

        return fraction + math.sin(SimulatedAnnealingTrigonometricExperimentData._cot(math.exp(fraction)))

    @staticmethod
    def _cot(x):
        epsilon = 1e-10
        return 1 / (math.tan(x) + epsilon)
