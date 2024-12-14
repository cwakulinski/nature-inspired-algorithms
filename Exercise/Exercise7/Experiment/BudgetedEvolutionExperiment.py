import numpy as np


class BudgetedEvolutionExperiment:
    def __init__(self):
        self._evaluation_function_name = None

        self._budget = None
        self._known_minimum = None
        self._algorithm_instance = None
        self._algorithm_instance_template = None


    def get_values_representation_type(self):
        return self._algorithm_instance_template.get_values_representation_type()

    def get_dimension_size(self):
        return self._algorithm_instance_template.dimension_size

    def get_name(self):
        return f"{self._evaluation_function_name}_dimension-{self.get_dimension_size()}_budget-{self._budget}"

    def execute(self):
        self._recreate_algorithm_instances()
        return self.generate_experiment_content()

    def _recreate_algorithm_instances(self):
        self._algorithm_instance = self._algorithm_instance_template.clone()

    def generate_experiment_content(self):
        output = ""
        best_value = float("inf")

        while True:
            evaluation_function_count = self._get_evaluation_function_call_count()

            if evaluation_function_count >= self._budget:
                break

            print(f"name {self.get_name()} (evaluation count {evaluation_function_count})")

            current_output = self._generate_next_evaluation_output()


            if current_output < best_value:
                best_value = current_output

            output += f"{evaluation_function_count}\t{best_value}\n"

        return output

    def _generate_next_evaluation_output(self):
        return np.abs(self._known_minimum - self._algorithm_instance.perform_step())

    def _get_evaluation_function_call_count(self):
        return self._algorithm_instance.evaluation_function_call_counter

    class Builder:
        def __init__(self):
            self._experiment_instance = BudgetedEvolutionExperiment()

        def set_budget(self, budget):
            self._experiment_instance._budget = budget

            return self

        def set_known_minimum(self, known_minimum):
            self._experiment_instance._known_minimum = known_minimum

            return self

        def set_evaluation_function_name(self, evaluation_function_name):
            self._experiment_instance._evaluation_function_name = evaluation_function_name

            return self

        def set_experiment_algorithm_instance(self, experiment_algorithm_instance):
            self._experiment_instance._algorithm_instance_template = experiment_algorithm_instance

            return self

        def build(self):
            return self._experiment_instance
