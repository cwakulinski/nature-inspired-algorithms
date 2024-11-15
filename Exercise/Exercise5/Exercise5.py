from Exercise.Exercise import Exercise
from Exercise.Exercise5.ExperimentFactory.ExperimentFactory import ExperimentFactory


class Exercise5(Exercise):
    def __init__(self):
        self._experiments = self._create_experiments_instances()

    @staticmethod
    def _create_experiments_instances():
        return [
            # ExperimentFactory().set_ackley_benchmark_function_variant().set_binary_representation_value().build(),
            ExperimentFactory().set_ackley_benchmark_function_variant().set_real_representation_value().build(),

            ExperimentFactory().set_sin_cot_function_variant().set_binary_representation_value().build(),
            ExperimentFactory().set_sin_cot_function_variant().set_real_representation_value().build(),
        ]

    def execute(self):
        for experiment in self._experiments:
            self._generate_experiment_file(experiment)

    def _generate_experiment_file(self, experiment_instance):
        file_name = self._generate_output_file_name(experiment_instance)
        experiment_content = experiment_instance.execute()

        with open(file_name, 'w') as file:
            file.write(experiment_content)

    @staticmethod
    def _generate_output_file_name(experiment_instance):
        output_file_name = \
            f"evolution_experiment_output_{experiment_instance.get_name()}.txt"

        return output_file_name
