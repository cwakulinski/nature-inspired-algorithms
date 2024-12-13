from Component.EvolutionaryAlgorithm.EvolutionaryAlgorithmPopulationIndividual.EvolutionaryAlgorithmPopulationIndividual import \
    EvolutionaryAlgorithmPopulationIndividual
from Component.RandomNumberGenerator.NormalDistNumberGenerator import NormalDistNumberGenerator


class EvolutionaryAlgorithmRealIndividual(EvolutionaryAlgorithmPopulationIndividual):
    def __init__(self):
        super().__init__()

    # Intermediate Recombination
    def crossover(self, other):
        # Intermediate recombination: offspring is the midpoint between parents
        child_value = [
            (self_val + other_val) / 2
            for self_val, other_val in zip(self._value, other.value)
        ]

        # Create child individual
        child = EvolutionaryAlgorithmRealIndividual.Builder() \
            .set_base_instance(self) \
            .set_value(child_value) \
            .build()

        return child

    # Gaussian Mutation
    def mutate(self, mutation_rate=0.1):
        gauss_generator = NormalDistNumberGenerator.Builder() \
            .set_mean(0) \
            .set_stddev(mutation_rate) \
            .build()

        mutated_value = [
            max(
                min(
                    x + gauss_generator.generate(),  # Add Gaussian noise
                    self._domain_upper_bound,
                ),
                self._domain_lower_bound,
            )
            for x in self._value
        ]

        mutated_individual = EvolutionaryAlgorithmRealIndividual.Builder() \
            .set_base_instance(self) \
            .set_value(mutated_value) \
            .build()

        return mutated_individual

    class Builder(EvolutionaryAlgorithmPopulationIndividual.Builder):
        def _create_instance(self):
            return EvolutionaryAlgorithmRealIndividual()