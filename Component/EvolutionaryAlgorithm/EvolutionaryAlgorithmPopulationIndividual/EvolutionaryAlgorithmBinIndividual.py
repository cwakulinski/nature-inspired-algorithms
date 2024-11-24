import random

import numpy as np

from Component.EvolutionaryAlgorithm.EvolutionaryAlgorithmPopulationIndividual.EvolutionaryAlgorithmPopulationIndividual import \
    EvolutionaryAlgorithmPopulationIndividual


class EvolutionaryAlgorithmBinIndividual(EvolutionaryAlgorithmPopulationIndividual):
    def __init__(self):
        super().__init__()

        self._value_bit_width = 16
        self._max_binary_value = (1 << self._value_bit_width) - 1

        # Computation caches
        self._bounds_range_precompute = None
        self._real_to_binary_factor_precompute = None
        self._binary_to_real_factor_precompute = None



    @property
    def _bounds_range(self):
        if self._bounds_range_precompute is None:
            self._bounds_range_precompute = self._domain_upper_bound - self._domain_lower_bound

        return  self._bounds_range_precompute

    @property
    def _real_to_binary_factor(self):
        if self._real_to_binary_factor_precompute is None:
            self._real_to_binary_factor_precompute = self._max_binary_value / self._bounds_range

        return self._real_to_binary_factor_precompute

    @property
    def _binary_to_real_factor(self):
        if self._binary_to_real_factor_precompute is None:
            self._binary_to_real_factor_precompute = self._bounds_range / self._max_binary_value

        return self._binary_to_real_factor_precompute

    @property
    def value(self):
        return self._binary_to_real(self._value)

    # One-point crossover
    def crossover(self, other):
        # Perform crossover for each dimension independently
        child_bin_value = []

        for x_self, x_other in zip(self._value, other._value):
            # Perform one-point crossover
            crossover_point = random.randint(1, self._value_bit_width - 1)

            # Mask to keep the left part of binary_self and right part of binary_other
            left_mask = (1 << crossover_point) - 1  # Mask for the leftmost `crossover_point` bits
            right_mask = ~left_mask & ((1 << self._value_bit_width) - 1)  # Mask for the rightmost bits

            # Apply the masks and shift appropriately
            left_part = x_self & left_mask  # Extract left part
            right_part = (x_other & right_mask)  # Extract right part

            # Combine the parts
            binary_value_part = (left_part) | (right_part)



            # Add the real value to the child's array
            child_bin_value.append(binary_value_part)

        # Create the child individual
        child = EvolutionaryAlgorithmBinIndividual.Builder() \
            .set_base_instance(self) \
            .set_value(self._binary_to_real(child_bin_value)) \
            .build()

        return child

    # Mutation using XOR Mask
    def mutate(self, mutation_rate=0.1):
        mutated_bin_value = []

        for x in self._value:
            # Iterate through each bit and flip based on mutation rate
            for index in range(self._value_bit_width):
                if random.random() <= mutation_rate:
                    # Flip the bit at the current index using XOR
                    x ^= (1 << index)

            mutated_bin_value.append(x)

        mutated_individual = EvolutionaryAlgorithmBinIndividual.Builder() \
            .set_base_instance(self) \
            .set_value(self._binary_to_real(mutated_bin_value)) \
            .build()

        return mutated_individual

    # def _real_to_binary(self, real_value):
    #     return int(self._real_to_binary_factor * (real_value - self._domain_lower_bound))
    #
    # def _binary_to_real(self, binary_value):
    #     return self._domain_lower_bound + binary_value  * self._binary_to_real_factor

    def _real_to_binary(self, real_values):
        return ((self._real_to_binary_factor * (np.array(real_values) - self._domain_lower_bound)).astype(int)).tolist()

    def _binary_to_real(self, binary_values):
        return (self._domain_lower_bound + np.array(binary_values) * self._binary_to_real_factor).tolist()

    # def _real_to_binary(self, x_value):
    #     normalized = int(
    #         ((x_value - self._domain_lower_bound) / (self._domain_upper_bound - self._domain_lower_bound)) * (
    #                 2 ** self._value_bit_width - 1))
    #     return normalized
    #
    # def _binary_to_real(self, binary_value):
    #     real_value = self._domain_lower_bound + (binary_value / (2 ** self._value_bit_width - 1)) * (
    #             self._domain_upper_bound - self._domain_lower_bound)
    #     return real_value

    class Builder(EvolutionaryAlgorithmPopulationIndividual.Builder):
        def _create_instance(self):
            return EvolutionaryAlgorithmBinIndividual()

        def build(self):
            instance = super().build()

            # instance._value = [instance._real_to_binary(value) for value in instance._value]
            instance._value = instance._real_to_binary(instance._value)

            return instance
