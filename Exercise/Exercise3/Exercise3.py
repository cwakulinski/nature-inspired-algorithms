from Exercise.Exercise import Exercise
from Exercise.Exercise3.LocalSearchContentGenerator import LocalSearchContentGenerator


class Exercise3(Exercise):
    def __init__(self):
        self._solution = 0

        self._lower_bound = -10
        self._upper_bound = 10

        self._dimensions = [2, 5, 10]

    def execute(self):
        for dimension_size in self._dimensions:
            self._create_output_file_by_dimension_size(dimension_size)

    def _create_output_file_by_dimension_size(self, dimension_size):
        file_name = f"local_search_output_n_{dimension_size}.txt"
        content_generator = self._create_content_generator_for_dimension_size(dimension_size)

        with open(file_name, 'w') as file:
            file.write(content_generator.generate())

    def _create_content_generator_for_dimension_size(self, dimension_size):
        return (LocalSearchContentGenerator.Builder()
                .set_solution_target(self._solution)
                .set_evaluation_function(self._evaluation_function)
                .set_lower_bound(self._lower_bound)
                .set_upper_bound(self._upper_bound)
                .set_staring_point(self._get_evaluation_function_starting_point(dimension_size))
                .build())

    def _get_evaluation_function_starting_point(self, dimension_size):
        return [self._upper_bound] * dimension_size

    @staticmethod
    def _evaluation_function(parameters):
        return sum(x ** 2 for x in parameters)
