import numpy as np

from Exercise.Exercise6.ExperimentFactory.EvolutionExperimentData.EvolutionExperimentECDFData import \
    EvolutionExperimentECDFData


class SinCotFunctionEvolutionExperimentECDFData(EvolutionExperimentECDFData):

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
        """
        Evaluate the function using NumPy for optimized computation.
        """
        # Convert parameters to a NumPy array
        parameters = np.asarray(parameters, dtype=np.float64)

        # Compute the denominator: 1 + sum(x^2 for x in parameters)
        denominator = 1 + np.sum(parameters ** 2)

        # Compute the fraction
        fraction = -5 / denominator

        # Clamp the fraction to the range [-700, 700]
        fraction = np.clip(fraction, -700, 700)

        # Compute the cotangent using NumPy
        cot_value = 1 / (np.tan(np.exp(fraction)) + 1e-10)

        # Final result: fraction + sin(cot(exp(fraction)))
        result = fraction + np.sin(cot_value)

        return result
    # def evaluation_function(self, parameters):
    #     numerator = -5
    #     denominator = 1 + sum(x ** 2 for x in parameters)
    #     fraction = numerator / denominator
    #
    #     if abs(fraction) > 700:
    #         fraction = math.copysign(700, fraction)
    #
    #     return fraction + math.sin(SinCotFunctionEvolutionExperimentData._cot(math.exp(fraction)))
    #
    # @staticmethod
    # def _cot(x):
    #     epsilon = 1e-10
    #     return 1 / (math.tan(x) + epsilon)
