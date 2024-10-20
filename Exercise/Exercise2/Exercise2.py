from Component.PiApproximator.PiApproximator import PiApproximator
from Exercise.Exercise import Exercise


def _create_approximation_entry_string(tries, pi_value):
    return f"{tries}	{pi_value}\n"


class _PiApproximationsFileManager:
    def __init__(self):
        self._file_name = 'pi_approximations.txt'

    def clear_file(self):
        open(self._file_name, 'w').close()

    def append_to_file(self, tries, pi_value):
        entry_to_append = _create_approximation_entry_string(tries, pi_value)

        with open(self._file_name, 'a') as file:
            file.write(entry_to_append)


class Exercise2(Exercise):
    def __init__(self):
        self._approximation_file_manager = _PiApproximationsFileManager()
        self._pi_approximator = PiApproximator()

        self._tries_counts_list = [1_000, 10_000, 100_000, 1_000_000]

    def _generate_pi_approximation_file(self):
        self._approximation_file_manager.clear_file()
        self._fill_pi_approximation_file()

    def _fill_pi_approximation_file(self):
        for tries_count in self._tries_counts_list:
            pi_value = self._pi_approximator.get_pi_approximation_by_monte_carlo_method(tries_count)
            self._approximation_file_manager.append_to_file(tries_count, pi_value)

    def execute(self):
        self._generate_pi_approximation_file()