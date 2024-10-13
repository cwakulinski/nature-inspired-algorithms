import random

from Component.RandomNumberGenerator.RandomNumberGenerator import RandomNumberGenerator


class NormalDistNumberGenerator(RandomNumberGenerator):
    def __init__(self):
        self._mean = 0
        self._stddev = 1

    def generate(self):
        return random.gauss(self._mean, self._stddev)

    class Builder:
        def __init__(self):
            self._dist = NormalDistNumberGenerator()

        def set_mean(self, mean):
            self._dist._mean = mean
            return self

        def set_stddev(self, stddev):
            self._dist._stddev = stddev
            return self

        def build(self):
            return self._dist
