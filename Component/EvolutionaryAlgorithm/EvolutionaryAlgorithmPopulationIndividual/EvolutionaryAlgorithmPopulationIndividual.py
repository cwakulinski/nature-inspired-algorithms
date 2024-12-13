from abc import ABC, abstractmethod

import copy

class EvolutionaryAlgorithmPopulationIndividual(ABC):
    def __init__(self):
        self._value = None # int[]

        self._evaluation_function_call_counter = 0 # f(...args)
        self._evaluation_function = None # f(...args)
        self._domain_lower_bound = None # int
        self._domain_upper_bound = None # int
        self._fitness = None #int

    def clone(self):
        # Create a new instance of the current class
        clone = self.__class__()
        # Copy all attributes dynamically
        for key, value in self.__dict__.items():
            if isinstance(value, list) and all(isinstance(i, int) for i in value):
                # Efficiently copy lists of integers (shallow copy is enough)
                setattr(clone, key, value[:])  # Slicing to create a new list
            elif isinstance(value, list):
                # Deep copy other lists
                setattr(clone, key, copy.deepcopy(value))
            elif callable(value) or isinstance(value, (int, float, str)):
                # Directly copy functions, numbers, and strings
                setattr(clone, key, value)
            else:
                # Shallow copy other attributes
                setattr(clone, key, copy.copy(value))
        return clone

    @abstractmethod
    def crossover(self, other):
        pass

    @abstractmethod
    def mutate(self, mutation_rate=0.1):
        pass

    @property
    def value(self):
        return self._value

    @property
    def fitness(self):
        if self._fitness is None:
            self._fitness = self._use_evaluation_function(self.value)

        return self._fitness

    @property
    def evaluation_function_call_counter(self):
        return self._evaluation_function_call_counter

    def _use_evaluation_function(self, args):
        self._evaluation_function_call_counter += 1

        return self._evaluation_function(args)

    class Builder:
        def __init__(self):
            self._built_instance = self._create_instance()

        def set_base_instance(self, base_instance):
            self._built_instance = base_instance.clone()

            return self

        def _create_instance(self):
            """
            Factory method to create the correct instance of the individual.
            Subclasses should override this to return the appropriate class.
            """
            raise NotImplementedError("Subclasses must implement this method.")

        def set_value(self, value):
            self._built_instance._value = value
            self._built_instance._fitness = None

            return self

        def set_evaluation_function(self, evaluation_function):
            self._built_instance._evaluation_function = evaluation_function
            self._built_instance._fitness = None

            return self

        def set_lower_bound(self, lower_bound):
            self._built_instance._domain_lower_bound = lower_bound
            return self

        def set_upper_bound(self, upper_bound):
            self._built_instance._domain_upper_bound = upper_bound
            return self

        def build(self):
            return self._built_instance
