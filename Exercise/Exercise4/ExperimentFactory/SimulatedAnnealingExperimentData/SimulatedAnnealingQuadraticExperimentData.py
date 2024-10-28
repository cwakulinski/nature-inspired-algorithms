import math

from Exercise.Exercise4.ExperimentFactory.SimulatedAnnealingExperimentData.SimulatedAnnealingExperimentData import \
    SimulatedAnnealingExperimentData


class SimulatedAnnealingQuadraticExperimentData(SimulatedAnnealingExperimentData):
    def __init__(self):
        self._evaluation_function_a_param = 20
        self._evaluation_function_b_param = 0.2
        self._evaluation_function_c_param = 2 * math.pi

    @property
    def name(self):
        return "quadratic"

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
        first_sum_term = self._get_first_term_of_evaluation_function(parameters)
        second_sum_term = self._get_second_term_of_evaluation_function(parameters)
        third_sum_term = self._evaluation_function_a_param
        fourth_sum_term = math.e

        return first_sum_term + second_sum_term + third_sum_term + fourth_sum_term


    def _get_first_term_of_evaluation_function(self, parameters):
        squares_sum = sum(x ** 2 for x in parameters)

        exp_arg = (-1) * self._evaluation_function_b_param * math.sqrt(squares_sum / self.dimensions)

        return math.exp(exp_arg) * (-1) * self._evaluation_function_a_param

    def _get_second_term_of_evaluation_function(self, parameters):
        cos_sum = sum(math.cos(self._evaluation_function_c_param * x) for x in parameters)

        exp_arg = cos_sum / self.dimensions

        return math.exp(exp_arg) * (-1)
