class EvolutionExperimentECDF:
    def __init__(self):
        self._evaluation_function_name = None
        self._representation_string = None

        self._algorithm_instances_list = None
        self._algorithm_instance_template = None

        self._algorithm_evaluations_per_run = 10_000
        self._algorithm_repeats_count = 100
        # self._algorithm_repeats_count = 1

        # self._algorithm_thresholds_count = 41
        # self._parallel_algorithms_count = 51

    def get_values_representation_type(self):
        return self._algorithm_instance_template.get_values_representation_type()

    def get_name(self):
        return f"{self._evaluation_function_name}_{self._representation_string}"

    def execute(self):
        self._recreate_algorithm_instances()
        return self.generate_experiment_content()

    def _recreate_algorithm_instances(self):
        self._algorithm_instances_list = \
            [self._algorithm_instance_template.clone() for _ in range(self._algorithm_repeats_count)]

    def generate_experiment_content(self):
        output = ""
        best_value = float("inf")

        for iteration_step_count in range(1, self._algorithm_evaluations_per_run + 1):
            print(f"name {self.get_name()} (iteration {iteration_step_count})")

            current_output = self._generate_next_evaluation_output()
            evaluation_function_count = self._get_evaluation_function_call_count()

            if current_output < best_value:
                best_value = current_output

            output += f"{iteration_step_count}\t{best_value}\t{evaluation_function_count}\n"

        return output

    def _generate_next_evaluation_output(self):
        outputs_sum = 0

        for algorithm_instance in self._algorithm_instances_list:
            outputs_sum += algorithm_instance.perform_step()

        return outputs_sum / self._algorithm_repeats_count

    def _get_evaluation_function_call_count(self):
        return self._algorithm_instances_list[0].evaluation_function_call_counter

    class Builder:
        def __init__(self):
            self._experiment_instance = EvolutionExperimentECDF()

        def set_representation_string(self, representation_string):
            self._experiment_instance._representation_string = representation_string

            return self

        def set_evaluation_function_name(self, evaluation_function_name):
            self._experiment_instance._evaluation_function_name = evaluation_function_name

            return self

        def set_experiment_algorithm_instance(self, experiment_algorithm_instance):
            self._experiment_instance._algorithm_instance_template = experiment_algorithm_instance

            return self

        def build(self):
            return self._experiment_instance
