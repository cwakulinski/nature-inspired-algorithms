import numpy as np

from Exercise.Exercise5.ExperimentFactory.EvolutionExperimentData.EvolutionExperimentData import EvolutionExperimentData

class AckleyBenchmarkFunctionEvolutionExperimentData(EvolutionExperimentData):
    def __init__(self):
        self._evaluation_function_a_param = 20
        self._evaluation_function_b_param = 0.2
        self._evaluation_function_c_param = 2 * np.pi

    @property
    def name(self):
        return "ackley_benchmark_function"

    @property
    def dimensions(self):
        return 10

    @property
    def lower_bound(self):
        return -32.768

    @property
    def upper_bound(self):
        return 32.768

    def evaluation_function(self, parameters):
        # Convert to NumPy array for vectorized operations
        parameters = np.array(parameters, dtype=np.float32)

        # Cache frequently used terms
        n = self.dimensions
        a = self._evaluation_function_a_param
        b = self._evaluation_function_b_param
        c = self._evaluation_function_c_param

        # Compute terms
        sum_squares = np.sum(parameters ** 2)
        sqrt_term = np.sqrt(sum_squares / n)
        first_term = -a * np.exp(-b * sqrt_term)

        cos_sum = np.sum(np.cos(c * parameters))
        second_term = -np.exp(cos_sum / n)

        # Add constants
        return first_term + second_term + a + np.e

    # def evaluation_function(self, parameters):
    #     first_sum_term = self._get_first_term_of_evaluation_function(parameters)
    #     second_sum_term = self._get_second_term_of_evaluation_function(parameters)
    #     third_sum_term = self._evaluation_function_a_param
    #     fourth_sum_term = math.e
    #
    #     return first_sum_term + second_sum_term + third_sum_term + fourth_sum_term
    #
    # def _get_first_term_of_evaluation_function(self, parameters):
    #     squares_sum = sum(x ** 2 for x in parameters)
    #
    #     exp_arg = (-1) * self._evaluation_function_b_param * math.sqrt(squares_sum / self.dimensions)
    #
    #     return math.exp(exp_arg) * (-1) * self._evaluation_function_a_param
    #
    # def _get_second_term_of_evaluation_function(self, parameters):
    #     cos_sum = sum(math.cos(self._evaluation_function_c_param * x) for x in parameters)
    #
    #     exp_arg = cos_sum / self.dimensions
    #
    #     return math.exp(exp_arg) * (-1)