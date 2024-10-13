from Component.RandomNumberGenerator.NormalDistNumberGenerator import NormalDistNumberGenerator
from Component.RandomNumberGenerator.UniformDistNumberGenerator import UniformDistNumberGenerator
from Exercise.Exercise import Exercise


def _save_dist_values_into_file(file_name, file_content):
    with open(file_name, 'w') as file:
        file.write(file_content)


class Exercise1(Exercise):
    def __init__(self):
        self._uniform_generator = UniformDistNumberGenerator.Builder().set_low(-1).set_high(1).build()
        self._gauss_generator = NormalDistNumberGenerator.Builder().set_mean(0).set_stddev(100).build()

        self._output_values_amount = 10_000

    def _generate_uniform_dist_values_file(self):
        generated_values = self._generate_file_content_for_distribution(self._uniform_generator)

        _save_dist_values_into_file('uniform_dist_values.txt', generated_values)

    def _generate_normal_dist_values_file(self):
        generated_values = self._generate_file_content_for_distribution(self._gauss_generator)

        _save_dist_values_into_file('normal_dist_values.txt', generated_values)

    def _generate_file_content_for_distribution(self, dist):
        return '\n'.join(str(dist.generate()) for _ in range(self._output_values_amount))

    def execute(self):
        self._generate_uniform_dist_values_file()
        self._generate_normal_dist_values_file()
