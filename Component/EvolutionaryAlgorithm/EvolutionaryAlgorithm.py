import copy
from enum import Enum
import random

from Component.EvolutionaryAlgorithm.EvolutionaryAlgorithmPopulationIndividual.EvolutionaryAlgorithmBinIndividual import \
    EvolutionaryAlgorithmBinIndividual
from Component.EvolutionaryAlgorithm.EvolutionaryAlgorithmPopulationIndividual.EvolutionaryAlgorithmRealIndividual import \
    EvolutionaryAlgorithmRealIndividual


class ValuesRepresentationType(Enum):
    REAL = "real"
    BINARY = "binary"


class EvolutionaryAlgorithm:
    def __init__(self):
        # Problem-specific properties

        self._evaluation_function_call_counter = 0
        self._values_representation_type = None
        self._current_base_population = None
        self._current_children_population = []


        # Representation and solutions
        self._current_best_fitness = float("inf")

    def perform_step(self):
        self._create_children_population()
        self._create_new_base_population()
        self._recalculate_current_best_fitness()

        return self._current_best_fitness  # Return best fitness so far

    @property
    def dimension_size(self):
        return len(self._current_base_population[0].value)

    @property
    def evaluation_function_call_counter(self):
        return self._evaluation_function_call_counter

    def _create_children_population(self):
        self._current_children_population = []

        for _ in range(len(self._current_base_population)):
            # Select two parents using tournament selection
            parent1 = self._tournament_selection(self._current_base_population)
            parent2 = self._tournament_selection(self._current_base_population)

            # Perform crossover to create a child
            child = parent1.crossover(parent2)

            mutated_child = child.mutate()

            # Append the new child to the children population
            self._current_children_population.append(mutated_child)


    def _tournament_selection(self, population, k=2, probability=0.9):
        # Randomly pick `k` individuals for the tournament
        tournament = random.sample(population, k)

        # Sort tournament participants by fitness ( the best first)
        tournament.sort(key=lambda ind: ind.fitness)

        # Select the winner probabilistically
        if random.random() < probability:
            return tournament[0]  # Best individual
        else:
            return random.choice(tournament[1:])  # Random from the rest

    def _create_new_base_population(self, elite_count=2):
        # Step 1: Sort the current base population by fitness (best first)
        self._current_base_population.sort(key=lambda ind: ind.fitness)

        # Step 2: Select the elite individuals
        elite_individuals = self._current_base_population[:elite_count]

        # Step 3: Combine the remaining base population and children population
        combined_population = (
                self._current_base_population[elite_count:] + self._current_children_population
        )

        # Step 4: Sort the combined population by fitness
        combined_population.sort(key=lambda ind: ind.fitness)

        # Step 5: Select individuals to fill the rest with the population (excluding elites)
        remaining_slots = len(self._current_base_population) - elite_count
        selected_individuals = combined_population[:remaining_slots]

        # Step 6: Update the base population with elites and selected individuals
        self._current_base_population = elite_individuals + selected_individuals

    def _recalculate_current_best_fitness(self):
        current_best_fitness = min(self._current_base_population, key=lambda ind: ind.fitness).fitness
        if current_best_fitness < self._current_best_fitness:
            self._current_best_fitness = current_best_fitness

    def get_values_representation_type(self):
        return self._values_representation_type.value

    def clone(self):
        copied_instance = copy.deepcopy(self)

        for individual in copied_instance._current_base_population:
            individual.update_evaluation_function_call_callback(
                lambda args: copied_instance._increment_evaluation_function_call_counter()
            )

        return copied_instance


    def _increment_evaluation_function_call_counter(self):
        self._evaluation_function_call_counter += 1

    class Builder:
        def __init__(self):

            self._evolutionary_algorithm_instance = EvolutionaryAlgorithm()

            self._evaluation_function = None


            self._domain_lower_bound = None
            self._domain_upper_bound = None

            self._population_size = None
            self._dimension_size = None


        def set_dimension_size(self, dimension_size):
            self._dimension_size = dimension_size
            return self

        def set_lower_bound(self, lower_bound):
            self._domain_lower_bound = lower_bound
            return self

        def set_upper_bound(self, upper_bound):
            self._domain_upper_bound = upper_bound
            return self

        def set_evaluation_function(self, evaluation_function):
            self._evaluation_function = evaluation_function

            return self

        def set_max_calls(self, max_calls):
            self._evolutionary_algorithm_instance._max_calls = max_calls

            return self

        def set_population_size(self, size):
            self._population_size = size
            return self

        def set_binary_representation_mode(self):
            self._evolutionary_algorithm_instance._values_representation_type = ValuesRepresentationType.BINARY
            return self

        def set_real_representation_mode(self):
            self._evolutionary_algorithm_instance._values_representation_type = ValuesRepresentationType.REAL
            return self

        def _construct_init_population(self):
            population = []

            individual_class = self._get_individual_class()

            # Generate individuals
            for _ in range(self._population_size):

                individual_value = [
                    random.uniform(self._domain_lower_bound, self._domain_upper_bound)
                    for _ in range(self._dimension_size)
                ]

                individual = individual_class.Builder() \
                    .set_value(individual_value) \
                    .set_evaluation_function(self._evaluation_function) \
                    .set_evaluation_function_call_callback(
                    lambda args: self._evolutionary_algorithm_instance._increment_evaluation_function_call_counter()
                ) \
                    .set_lower_bound(self._domain_lower_bound) \
                    .set_upper_bound(self._domain_upper_bound) \
                    .build()

                population.append(individual)

            return population

        def _get_individual_class(self):
            representation_type = self._evolutionary_algorithm_instance._values_representation_type

            if representation_type == ValuesRepresentationType.BINARY:
                return EvolutionaryAlgorithmBinIndividual
            elif representation_type == ValuesRepresentationType.REAL:
                return EvolutionaryAlgorithmRealIndividual
            else:
                raise NotImplementedError(f'Missing individual type for ${representation_type}')



        def build(self):
            self._evolutionary_algorithm_instance._current_base_population  = self._construct_init_population()

            return self._evolutionary_algorithm_instance
