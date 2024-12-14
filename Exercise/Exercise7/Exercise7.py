import os

from Exercise.Exercise import Exercise

from Exercise.Exercise7.ExperimentFactory.ExperimentFactory import BudgetedEvolutionExperimentFactory

class Exercise7(Exercise):
    def __init__(self):
        self._experiments = self._create_experiments_instances()

    @staticmethod
    def _create_experiments_instances():
        return BudgetedEvolutionExperimentFactory().ceateAllExperiments()

    def execute(self):
        for experiment in self._experiments:
            self._generate_experiment_file(experiment)

    def _generate_experiment_file(self, experiment_instance):
        # Ensure the './output' directory exists
        output_dir = "./output"
        os.makedirs(output_dir, exist_ok=True)

        # Generate the file name with the output directory
        file_name = os.path.join(output_dir, self._generate_output_file_name(experiment_instance))
        experiment_content = experiment_instance.execute()

        # Save the file in the './output' directory
        with open(file_name, 'w') as file:
            file.write(experiment_content)

    @staticmethod
    def _generate_output_file_name(experiment_instance):
        # Generate the output file name
        output_file_name = f"evolution_experiment_output_{experiment_instance.get_name()}.txt"
        return output_file_name
