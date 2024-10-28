import copy

from Component.RandomNumberGenerator.UniformDistNumberGenerator import UniformDistNumberGenerator


class FirstImprovementLocalSearch:
    def __init__(self):
        self._value_bit_width = 16
        self._uniform_generator = self._create_uniform_generator()

        self._evaluation_function = None
        self._domain_lower_bound = None
        self._domain_upper_bound = None
        self._target_solution = None
        self._current_point = None

        self._current_solution_estimate = None

    @staticmethod
    def _create_uniform_generator():
        return (UniformDistNumberGenerator.Builder()
                .set_generate_only_whole_numbers()
                .set_low(0)
                .set_high(15)
                .build()
                )

    def perform_step(self):
        self._try_to_refine_solution()

        return self._current_solution_estimate

    def _try_to_refine_solution(self):
        new_point_to_check = self._generate_next_search_point()
        evaluation_function_output = self._evaluation_function(new_point_to_check)

        if not self._is_valid_evaluation(evaluation_function_output):
            return

        self._current_solution_estimate = evaluation_function_output
        self._current_point = new_point_to_check

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

            # Convert x_value to binary and flip a random bit
            binary_x = self._real_to_binary(x_value)
            bit_to_flip = 1 << self._uniform_generator.generate()  # Assuming 16-bit representation
            new_binary_x = binary_x ^ bit_to_flip

            # Convert back to real value and check bounds
            new_x_value = self._binary_to_real(new_binary_x)
            if self._is_num_in_bounds(new_x_value):
                return new_x_value

        return x_value  # Return original if no valid neighbor found

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

    def _is_valid_evaluation(self, new_evaluation_value):
        if self._current_solution_estimate is None:
            return True

        return abs(self._target_solution - self._current_solution_estimate) > abs(
            self._target_solution - new_evaluation_value)

    def clone(self):
        return copy.deepcopy(self)

    class Builder:
        def __init__(self):
            self._local_search_instance = FirstImprovementLocalSearch()

        def set_evaluation_function(self, evaluation_function):
            self._local_search_instance._evaluation_function = evaluation_function
            return self

        def set_domain_lower_bound(self, lower_bound):
            self._local_search_instance._domain_lower_bound = lower_bound
            return self

        def set_domain_upper_bound(self, upper_bound):
            self._local_search_instance._domain_upper_bound = upper_bound
            return self

        def set_target_solution(self, target_solution):
            self._local_search_instance._target_solution = target_solution
            return self

        def set_starting_point(self, starting_point):
            self._local_search_instance._current_point = starting_point
            return self

        def build(self):
            return self._local_search_instance
