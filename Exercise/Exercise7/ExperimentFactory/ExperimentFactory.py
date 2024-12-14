import numpy as np

from Component.EvolutionaryAlgorithm.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from Exercise.Exercise7.Experiment.BudgetedEvolutionExperiment import BudgetedEvolutionExperiment
from Exercise.Exercise7.ExperimentFactory.EvolutionExperimentData.RosenbrockBudgetedEvolutionExperimentData import \
    RosenbrockBudgetedEvolutionExperimentData
from Exercise.Exercise7.ExperimentFactory.EvolutionExperimentData.SalomonBudgetedEvolutionExperimentData import \
    SalomonBudgetedEvolutionExperimentData
from Exercise.Exercise7.ExperimentFactory.EvolutionExperimentData.WhitleyBudgetedEvolutionExperimentData import \
    WhitleyBudgetedEvolutionExperimentData


class BudgetedEvolutionExperimentFactory:
    def __init__(self):
        self._budget_count = 100
        self._dimensions = [5, 15, 30]
        self._experiment_functions_data = [
            RosenbrockBudgetedEvolutionExperimentData(),
            SalomonBudgetedEvolutionExperimentData(),
            WhitleyBudgetedEvolutionExperimentData()
        ]

    def ceateAllExperiments(self):
        output = []

        for experiment_data in self._experiment_functions_data:
            for dimension in self._dimensions:
                for budget_count in range(self._budget_count):
                    evolutionary_algorithm_builder = (
                        EvolutionaryAlgorithm.Builder()
                        .set_real_representation_mode()
                        .set_dimension_size(dimension)
                        .set_lower_bound(experiment_data.lower_bound)
                        .set_upper_bound(experiment_data.upper_bound)
                        .set_evaluation_function(experiment_data.evaluation_function)
                        .set_population_size(experiment_data.population_size)
                    )

                    budgeted_evolution_experiment_builder = (
                        BudgetedEvolutionExperiment.Builder()
                        .set_experiment_algorithm_instance(evolutionary_algorithm_builder.build())
                        .set_known_minimum(experiment_data.known_minimum)
                        .set_budget(
                            self._get_nth_cost_value(budget_count)
                        )
                        .set_evaluation_function_name(experiment_data.name)
                    )

                    output.append(budgeted_evolution_experiment_builder.build())

        return output

    def _get_nth_cost_value(self, n):
        return int(np.floor(np.power(10, -8 + 0.2 * n)))
