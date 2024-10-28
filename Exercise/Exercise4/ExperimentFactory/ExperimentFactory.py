from Component.SimulatedAnnealing.SimulatedAnnealing import SimulatedAnnealing
from Exercise.Exercise4.Experiment.SimulatedAnnealingExperiment import SimulatedAnnealingExperiment
from Exercise.Exercise4.ExperimentFactory.SimulatedAnnealingExperimentData.SimulatedAnnealingQuadraticExperimentData import \
    SimulatedAnnealingQuadraticExperimentData
from Exercise.Exercise4.ExperimentFactory.SimulatedAnnealingExperimentData.SimulatedAnnealingTrigonometricExperimentData import \
    SimulatedAnnealingTrigonometricExperimentData


class ExperimentFactory:
    def __init__(self):
        self.experiment_builder = SimulatedAnnealingExperiment.Builder()
        self.experiment_algorithm_builder = SimulatedAnnealing.Builder()

    def set_real_representation_value(self):
        self.experiment_builder.set_representation_string('real')
        self.experiment_algorithm_builder.set_real_representation_mode()

        return self

    def set_binary_representation_value(self):
        self.experiment_builder.set_representation_string('binary')
        self.experiment_algorithm_builder.set_binary_representation_mode()

        return self

    def set_quadratic_annealing_variant(self):
        data_instance = SimulatedAnnealingQuadraticExperimentData()

        self._apply_experiment_data_instance(data_instance)

        return self

    def set_trigonometric_annealing_variant(self):
        data_instance = SimulatedAnnealingTrigonometricExperimentData()

        self._apply_experiment_data_instance(data_instance)

        return self

    def _apply_experiment_data_instance(self, data_instance):
        self.experiment_builder.set_evaluation_function_name(data_instance.name)
        self.experiment_algorithm_builder.set_dimension_size(data_instance.dimensions)
        self.experiment_algorithm_builder.set_lower_bound(data_instance.lower_bound)
        self.experiment_algorithm_builder.set_upper_bound(data_instance.upper_bound)
        self.experiment_algorithm_builder.set_evaluation_function(data_instance.evaluation_function)
        self.experiment_algorithm_builder.set_starting_point(data_instance.starting_point)

    def build(self):
        self.experiment_builder.set_experiment_algorithm_instance(
            self.experiment_algorithm_builder.build()
        )

        return self.experiment_builder.build()
