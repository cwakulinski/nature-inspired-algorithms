from Component.FirstImprovementLocalSearch.FirstImprovementLocalSearch import FirstImprovementLocalSearch


class LocalSearchContentGenerator:
    def __init__(self):
        self._local_search_instance_template = None
        self._local_search_instances_list = None

        self._algorithm_evaluations_per_run = 10_000
        self._algorithm_repeats_count = 100

    def generate(self):
        self._recreate_local_search_instances()
        return self.generate_content_from_search_instances()

    def _recreate_local_search_instances(self):
        self._local_search_instances_list = \
            [self._local_search_instance_template.clone() for _ in range(self._algorithm_repeats_count)]

    def generate_content_from_search_instances(self):
        output = ""

        for iteration_step_count in range(1, self._algorithm_evaluations_per_run + 1):
            output += f"{iteration_step_count}	{self._generate_next_evaluation_output()}\n"

        return output

    def _generate_next_evaluation_output(self):
        local_search_outputs_sum = 0

        for local_search_instance in self._local_search_instances_list:
            local_search_outputs_sum += local_search_instance.perform_step()

        return local_search_outputs_sum / self._algorithm_repeats_count

    class Builder:
        def __init__(self):
            self._first_improvement_local_search_builder = FirstImprovementLocalSearch.Builder()
            self._generator_instance = LocalSearchContentGenerator()

        def set_evaluation_function(self, evaluation_function):
            self._first_improvement_local_search_builder.set_evaluation_function(evaluation_function)

            return self

        def set_lower_bound(self, lower_bound):
            self._first_improvement_local_search_builder.set_domain_lower_bound(lower_bound)

            return self

        def set_upper_bound(self, upper_bound):
            self._first_improvement_local_search_builder.set_domain_upper_bound(upper_bound)

            return self

        def set_solution_target(self, solution):
            self._first_improvement_local_search_builder.set_target_solution(solution)

            return self

        def set_staring_point(self, starting_point):
            self._first_improvement_local_search_builder.set_starting_point(starting_point)

            return self

        def build(self):
            self._generator_instance._local_search_instance_template = self._first_improvement_local_search_builder.build()

            return self._generator_instance
