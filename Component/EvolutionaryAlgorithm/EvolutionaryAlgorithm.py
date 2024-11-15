import copy
import math
from enum import Enum

from Component.RandomNumberGenerator.NormalDistNumberGenerator import NormalDistNumberGenerator
from Component.RandomNumberGenerator.UniformDistNumberGenerator import UniformDistNumberGenerator


class ValuesRepresentationType(Enum):
    REAL = "real"
    BINARY = "binary"


class EvolutionaryAlgorithm:
    def __init__(self):
        self._value_bit_width = 16  # Bit width for binary representation

        # Random number generators
        self._int_generator = self._create_int_generator()
        self._gauss_generator = self._create_gauss_generator()
        self._uniform_zero_to_one_float_generator = self._create_float_generator()

        # Problem-specific properties
        self._evaluation_function = None
        self._domain_lower_bound = None
        self._domain_upper_bound = None
        self._current_population = None

        # Representation and solutions
        self._values_representation_type = None
        self._current_best_fitness = None
        self._best_solution = None
        self._tau = .5  # Learning rate for step size mutation

    @staticmethod
    def _create_gauss_generator():
        return NormalDistNumberGenerator.Builder() \
            .set_mean(0) \
            .set_stddev(1) \
            .build()

    @staticmethod
    def _create_int_generator():
        return UniformDistNumberGenerator.Builder() \
            .set_generate_only_whole_numbers() \
            .set_low(0) \
            .set_high(15) \
            .build()

    @staticmethod
    def _create_float_generator():
        return UniformDistNumberGenerator.Builder() \
            .set_low(0) \
            .set_high(1) \
            .build()

    def perform_step(self):
        self._evaluate_population()
        self._mutate_population()

        return self._current_best_fitness  # Return best fitness so far

    def _mutate_population(self):
        # Adjust each individual in the population
        new_population = []
        for individual, sigma in self._current_population:
            mutated_individual, mutated_sigma = self._mutate_individual(individual, sigma)
            new_population.append((mutated_individual, mutated_sigma))
        self._current_population = new_population

    def _mutate_individual(self, individual, sigma):
        # Uncorrelated Mutation with One Step Size
        # Mutate the step size (sigma)

        if self._values_representation_type == ValuesRepresentationType.BINARY:
            # For binary representation, σ is irrelevant
            mutated_sigma = sigma
        else:
            # Mutate the step size (σ) for real-valued representation
            mutated_sigma = sigma * math.exp(self._tau * self._gauss_generator.generate())


            # Mutate each gene in the individual
        mutated_individual = []
        for gene in individual:
            if self._values_representation_type == ValuesRepresentationType.BINARY:
                # Binary mutation: Flip a random bit
                mutated_gene = self._mutate_binary_gene(gene)
            else:
                # Real-valued mutation: Add Gaussian noise scaled by σ
                mutated_gene = gene + self._gauss_generator.generate() * mutated_sigma
            mutated_individual.append(mutated_gene)

        return mutated_individual, mutated_sigma

    def _mutate_binary_gene(self, gene):
        binary_gene = self._real_to_binary(gene)
        bit_to_flip = 1 << self._int_generator.generate()
        new_binary_gene = binary_gene ^ bit_to_flip
        return self._binary_to_real(new_binary_gene)

    def _evaluate_population(self):
        best_fitness = float("inf")

        for individual, sigma in self._current_population:
            fitness = self._evaluation_function(individual)
            if fitness < best_fitness:
                best_fitness = fitness
                self._best_solution = individual
        self._current_best_fitness = best_fitness

    def _real_to_binary(self, value):
        normalized = int(
            ((value - self._domain_lower_bound) / (self._domain_upper_bound - self._domain_lower_bound)) * (
                    2 ** self._value_bit_width - 1))
        return normalized

    def _binary_to_real(self, binary_value):
        return self._domain_lower_bound + (binary_value / (2 ** self._value_bit_width - 1)) * (
                self._domain_upper_bound - self._domain_lower_bound)

    def get_values_representation_type(self):
        return self._values_representation_type.value

    def clone(self):
        return copy.deepcopy(self)

    class Builder:
        def __init__(self):
            self._evolutionary_algorithm_instance = EvolutionaryAlgorithm()
            self._population_size = None

        def set_dimension_size(self, dimension_size):
            self._evolutionary_algorithm_instance._dimension = dimension_size
            return self

        def set_lower_bound(self, lower_bound):
            self._evolutionary_algorithm_instance._domain_lower_bound = lower_bound
            return self

        def set_upper_bound(self, upper_bound):
            self._evolutionary_algorithm_instance._domain_upper_bound = upper_bound
            return self

        def set_evaluation_function(self, evaluation_function):
            self._evolutionary_algorithm_instance._evaluation_function = evaluation_function
            return self

        def set_binary_representation_mode(self):
            self._evolutionary_algorithm_instance._values_representation_type = ValuesRepresentationType.BINARY
            return self

        def set_real_representation_mode(self):
            self._evolutionary_algorithm_instance._values_representation_type = ValuesRepresentationType.REAL
            return self

        def set_init_population(self, population):
            # Initialize each individual as a tuple (x, sigma), where sigma starts at a reasonable value
            initial_sigma = 1.0  # Default initial step size for all individuals
            self._evolutionary_algorithm_instance._current_population = [(ind, initial_sigma) for ind in population]
            return self

        def build(self):
            return self._evolutionary_algorithm_instance
