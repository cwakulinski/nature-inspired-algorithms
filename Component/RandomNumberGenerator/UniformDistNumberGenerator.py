import random

from Component.RandomNumberGenerator.RandomNumberGenerator import RandomNumberGenerator


class UniformDistNumberGenerator(RandomNumberGenerator):
    def __init__(self):
        self._low = 0
        self._high = 1

    def generate(self):
        return random.uniform(self._low, self._high)

    class Builder:
        def __init__(self):
            self._dist = UniformDistNumberGenerator()

        def set_low(self, low):
            self._dist._low = low
            return self

        def set_high(self, high):
            self._dist._high = high
            return self

        def build(self):
            return self._dist
