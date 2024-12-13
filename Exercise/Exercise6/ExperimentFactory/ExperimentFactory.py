from Component.EvolutionaryAlgorithm.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from Exercise.Exercise6.Experiment.EvolutionExperimentECDF import EvolutionExperimentECDF

from Exercise.Exercise6.ExperimentFactory.EvolutionExperimentData.AckleyBenchmarkFunctionEvolutionExperimentECDFData import \
    AckleyBenchmarkFunctionEvolutionExperimentECDFData
from Exercise.Exercise6.ExperimentFactory.EvolutionExperimentData.SinCotFunctionEvolutionExperimentECDFData import \
    SinCotFunctionEvolutionExperimentECDFData


class EvolutionExperimentECDFFactory:
    def __init__(self):
        self.experiment_builder = EvolutionExperimentECDF.Builder()
        self.experiment_algorithm_builder = EvolutionaryAlgorithm.Builder()

    def set_real_representation_value(self):
        self.experiment_builder.set_representation_string('real')
        self.experiment_algorithm_builder.set_real_representation_mode()

        return self

    def set_binary_representation_value(self):
        self.experiment_builder.set_representation_string('binary')
        self.experiment_algorithm_builder.set_binary_representation_mode()

        return self

    def set_ackley_benchmark_function_variant(self):
        data_instance = AckleyBenchmarkFunctionEvolutionExperimentECDFData()

        self._apply_experiment_data_instance(data_instance)

        return self

    def set_sin_cot_function_variant(self):
        data_instance = SinCotFunctionEvolutionExperimentECDFData()

        self._apply_experiment_data_instance(data_instance)

        return self

    def _apply_experiment_data_instance(self, data_instance):
        self.experiment_builder.set_evaluation_function_name(data_instance.name)
        self.experiment_algorithm_builder.set_dimension_size(data_instance.dimensions)
        self.experiment_algorithm_builder.set_lower_bound(data_instance.lower_bound)
        self.experiment_algorithm_builder.set_upper_bound(data_instance.upper_bound)
        self.experiment_algorithm_builder.set_evaluation_function(data_instance.evaluation_function)
        self.experiment_algorithm_builder.set_population_size(data_instance.population_size)

    def build(self):
        self.experiment_builder.set_experiment_algorithm_instance(
            self.experiment_algorithm_builder.build()
        )

        return self.experiment_builder.build()
