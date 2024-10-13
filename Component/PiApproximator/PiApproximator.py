import math
from Component.RandomNumberGenerator.UniformDistNumberGenerator import UniformDistNumberGenerator


class PiApproximator:
    def __init__(self):
        self._uniform_generator = UniformDistNumberGenerator.Builder().set_low(-1).set_high(1).build()

    def get_pi_approximation_by_monte_carlo_method(self, throws):
        hit_amount = 0

        for i in range(throws):
            x, y = self._uniform_generator.generate(), self._uniform_generator.generate()

            dist_from_center = math.sqrt(math.pow(x, 2) + math.pow(y, 2))

            if dist_from_center <= 1:
                hit_amount += 1

        return 4 * hit_amount / throws
