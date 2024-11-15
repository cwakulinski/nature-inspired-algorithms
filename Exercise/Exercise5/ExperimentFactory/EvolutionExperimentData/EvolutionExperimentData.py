from abc import ABC, abstractmethod

from Component.RandomNumberGenerator.UniformDistNumberGenerator import UniformDistNumberGenerator


class EvolutionExperimentData(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def dimensions(self):
        pass

    @property
    def population_size(self):
        return 100

    def get_init_population(self):
        population = []

        u_rng = UniformDistNumberGenerator.Builder() \
            .set_low(0) \
            .set_high(1) \
            .build()

        for _ in range(self.population_size):
            # Generate an individual with random values for each dimension

            individual = [
                u_rng.generate() *
                (self.upper_bound -
                 self.lower_bound) +
                self.lower_bound
                for _ in range(self.dimensions)
            ]

            population.append(individual)
        return population

    @property
    @abstractmethod
    def lower_bound(self):
        pass

    @property
    @abstractmethod
    def upper_bound(self):
        pass

    @abstractmethod
    def evaluation_function(self, parameters):
        pass
