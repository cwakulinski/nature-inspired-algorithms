import copy
import math
from enum import Enum

from Component.RandomNumberGenerator.NormalDistNumberGenerator import NormalDistNumberGenerator
from Component.RandomNumberGenerator.UniformDistNumberGenerator import UniformDistNumberGenerator


class ValuesRepresentationType(Enum):
    REAL = "real"
    BINARY = "binary"


class SimulatedAnnealing:
    def __init__(self):
        self._value_bit_width = 16

        self._cooling_rate = 0.99
        self._temperature = 100

        self._int_generator = self._create_int_generator()
        self._gauss_generator = self._create_gauss_generator()
        self._uniform_zero_to_one_float_generator = self._create_float_generator()

        self._evaluation_function = None
        self._domain_lower_bound = None
        self._domain_upper_bound = None
        self._current_point = None

        self._values_representation_type = None
        self._current_solution_estimate = None
        self._best_solution_estimate = None

    @staticmethod
    def _create_gauss_generator():
        return NormalDistNumberGenerator.Builder() \
            .set_mean(0) \
            .set_stddev(1) \
            .build()

    @staticmethod
    def _create_int_generator():
        return UniformDistNumberGenerator.Builder() \
            .set_generate_only_whole_numbers() \
            .set_low(0) \
            .set_high(15) \
            .build()

    @staticmethod
    def _create_float_generator():
        return UniformDistNumberGenerator.Builder() \
            .set_low(0) \
            .set_high(1) \
            .build()

    def perform_step(self):
        self._try_to_refine_solution()
        self._cool_down()
        return self._best_solution_estimate  # Return best found so far

    def _try_to_refine_solution(self):
        new_point_to_check = self._generate_next_search_point()
        evaluation_function_output = self._evaluation_function(new_point_to_check)

        if not self._accept_new_solution(evaluation_function_output):
            return

        self._current_solution_estimate = evaluation_function_output
        self._current_point = new_point_to_check

        if self._best_solution_estimate is None or evaluation_function_output < self._best_solution_estimate:
            self._best_solution_estimate = evaluation_function_output

    def _accept_new_solution(self, new_solution_estimate):
        if self._current_solution_estimate is None:
            return True

        delta = new_solution_estimate - self._current_solution_estimate
        if delta < 0:
            return True  # Accept better solutions unconditionally

        # Accept worse solutions with probability based on temperature
        acceptance_probability = math.exp(-delta / self._temperature)
        return self._uniform_zero_to_one_float_generator.generate() < acceptance_probability

    def _generate_next_search_point(self):
        output_point = []
        for x in self._current_point:
            adjusted_x_value = self._try_adjusting_single_x_arg_into_neighbour_value(x)
            output_point.append(adjusted_x_value)
        return output_point

    def _try_adjusting_single_x_arg_into_neighbour_value(self, x_value):
        fail_safe_counter = 1_000

        while fail_safe_counter:
            fail_safe_counter -= 1

            if self._values_representation_type == ValuesRepresentationType.BINARY:
                new_x_value = self._adjust_binary_neighbor(x_value)
            else:
                new_x_value = self._adjust_real_neighbor(x_value)

            if self._is_num_in_bounds(new_x_value):
                return new_x_value

        return x_value

    def _adjust_binary_neighbor(self, x_value):
        binary_x = self._real_to_binary(x_value)
        bit_to_flip = 1 << self._int_generator.generate()
        new_binary_x = binary_x ^ bit_to_flip

        return self._binary_to_real(new_binary_x)

    def _adjust_real_neighbor(self, x_value):
        return x_value + self._gauss_generator.generate()

    def _real_to_binary(self, x_value):
        normalized = int(
            ((x_value - self._domain_lower_bound) / (self._domain_upper_bound - self._domain_lower_bound)) * (
                    2 ** self._value_bit_width - 1))
        return normalized

    def _binary_to_real(self, binary_value):
        real_value = self._domain_lower_bound + (binary_value / (2 ** self._value_bit_width - 1)) * (
                self._domain_upper_bound - self._domain_lower_bound)
        return real_value

    def _is_num_in_bounds(self, num):
        return self._domain_lower_bound <= num <= self._domain_upper_bound

    def _cool_down(self):
        self._temperature *= self._cooling_rate

    def get_values_representation_type(self):
        return self._values_representation_type.value

    def clone(self):
        return copy.deepcopy(self)

    class Builder:
        def __init__(self):
            self._simulated_annealing_instance = SimulatedAnnealing()

        def set_dimension_size(self, dimension_size):
            self._simulated_annealing_instance._dimension = dimension_size
            return self

        def set_lower_bound(self, lower_bound):
            self._simulated_annealing_instance._domain_lower_bound = lower_bound
            return self

        def set_upper_bound(self, upper_bound):
            self._simulated_annealing_instance._domain_upper_bound = upper_bound
            return self

        def set_evaluation_function(self, evaluation_function):
            self._simulated_annealing_instance._evaluation_function = evaluation_function
            return self

        def set_binary_representation_mode(self):
            self._simulated_annealing_instance._values_representation_type = ValuesRepresentationType.BINARY
            return self

        def set_real_representation_mode(self):
            self._simulated_annealing_instance._values_representation_type = ValuesRepresentationType.REAL
            return self

        def set_starting_point(self, starting_point):
            self._simulated_annealing_instance._current_point = starting_point

            self._simulated_annealing_instance._current_solution_estimate = \
                self._simulated_annealing_instance._evaluation_function(starting_point)
            self._simulated_annealing_instance._best_solution_estimate = \
                self._simulated_annealing_instance._current_solution_estimate

            return self

        def build(self):
            return self._simulated_annealing_instance
