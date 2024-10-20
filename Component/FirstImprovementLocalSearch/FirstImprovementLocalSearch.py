import copy

from Component.RandomNumberGenerator.UniformDistNumberGenerator import UniformDistNumberGenerator


class FirstImprovementLocalSearch:
    def __init__(self):
        self._uniform_generator = UniformDistNumberGenerator.Builder().set_low(-1).set_high(1).build()

        self._evaluation_function = None
        self._domain_lower_bound = None
        self._domain_upper_bound = None
        self._target_solution = None
        self._current_point = None

        self._current_solution_estimate = None


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
        fail_save_counter = 1_000

        while fail_save_counter:
            fail_save_counter -= 1
            new_x_value = x_value + self._uniform_generator.generate()

            if not self._is_num_in_bounds(new_x_value):
                continue

            return new_x_value

        return x_value

    def _is_num_in_bounds(self, num):
        return self._domain_lower_bound <= num <= self._domain_upper_bound

    def _is_valid_evaluation(self, new_evaluation_value):
        if self._current_solution_estimate is None:
            return True

        return abs(self._target_solution - self._current_solution_estimate) > abs(self._target_solution - new_evaluation_value)

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


