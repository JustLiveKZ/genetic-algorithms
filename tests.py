import unittest

from chromosome import Chromosome
from manager import ChromosomeManager


class ChromosomeTestCase(unittest.TestCase):
    chromosome = None

    def setUp(self):
        self.chromosome = Chromosome()

    def test_str(self):
        self.chromosome.binary_string = '010111000011101100101010011111010100'
        self.assertEqual(str(self.chromosome), '010111000011101100101010011111010100')

    def test_evaluation_with_correct_data(self):
        self.chromosome.binary_string = '010111000011101100101010011111010100'
        self.chromosome.evaluate(5)
        self.assertEqual(self.chromosome.result, 5)
        self.assertEqual(self.chromosome.score, 1e18)

    def test_evaluation_with_incorrect_data(self):
        self.chromosome.binary_string = '111111111111111111111111111111111111'
        self.chromosome.evaluate(20)
        self.assertEqual(self.chromosome.result, 0)
        self.assertEqual(self.chromosome.score, 0.05)

    def test_evaluation_with_correct_and_incorrect_data(self):
        self.chromosome.binary_string = '011011100001101010110101100110111100'
        self.chromosome.evaluate(10)
        self.assertEqual(self.chromosome.result, 11)
        self.assertEqual(self.chromosome.score, 1)

    def test_evaluation_with_zero_division(self):
        self.chromosome.binary_string = '001011111111111111111111110111110000'
        self.chromosome.evaluate(5)
        self.assertEqual(self.chromosome.result, 2)
        self.assertEqual(self.chromosome.score, 1 / 3)

    def test_fill_with_random_values(self):
        self.chromosome.fill_with_random_values()
        self.assertEqual(len(self.chromosome.binary_string), 36)
        for char in self.chromosome.binary_string:
            self.assertTrue(0 <= int(char) <= 1)

    def test_mutate(self):
        original_binary_string = '010111000011101100101010011111010100'
        self.chromosome.binary_string = original_binary_string
        mutated_chars = self.chromosome.mutate(0.1)
        levenshtein_distance = self._get_levenshtein_distance(original_binary_string, self.chromosome.binary_string)
        self.assertEqual(mutated_chars, levenshtein_distance)

    def test_mutate_full(self):
        original_binary_string = '010111000011101100101010011111010100'
        reversed_string = '101000111100010011010101100000101011'
        self.chromosome.binary_string = original_binary_string
        mutated_chars = self.chromosome.mutate(1)
        self.assertEqual(mutated_chars, 36)
        self.assertEqual(self.chromosome.binary_string, reversed_string)

    def _get_levenshtein_distance(self, string1, string2):
        self.assertEqual(len(string1), len(string2))
        length = len(string1)
        different_chars_count = 0
        for i in range(0, length):
            if string1[i] != string2[i]:
                different_chars_count += 1
        return different_chars_count


class ChromosomeManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.chromosome_manager = ChromosomeManager()

    def test_generate_first_generation(self):
        self.chromosome_manager.generate_first_generation()
        self.assertEqual(len(self.chromosome_manager.chromosomes), 10)

    def test_get_index(self):
        probabilities = [0.1, 0.05, 0.1, 0.2, 0.5, 0.05]
        self.assertEqual(self.chromosome_manager.get_index(0.07, probabilities), 0)
        self.assertEqual(self.chromosome_manager.get_index(0.1, probabilities), 0)
        self.assertEqual(self.chromosome_manager.get_index(0.11, probabilities), 1)
        self.assertEqual(self.chromosome_manager.get_index(0.25, probabilities), 2)
        self.assertEqual(self.chromosome_manager.get_index(0.38, probabilities), 3)
        self.assertEqual(self.chromosome_manager.get_index(0.73, probabilities), 4)
        self.assertEqual(self.chromosome_manager.get_index(0.96, probabilities), 5)
        self.assertEqual(self.chromosome_manager.get_index(1, probabilities), 5)

    def test_roulette_wheel(self):
        self.chromosome_manager.generate_first_generation()
        for chromosome in self.chromosome_manager.chromosomes:
            chromosome.evaluate(self.chromosome_manager.target_value)
        chromosome1, chromosome2 = self.chromosome_manager.do_roulette_wheel()
        self.assertNotEqual(chromosome1, chromosome2)
        self.assertIn(chromosome1, self.chromosome_manager.chromosomes)
        self.assertIn(chromosome2, self.chromosome_manager.chromosomes)

    def test_crossover(self):
        self.chromosome_manager.generate_first_generation()
        for chromosome in self.chromosome_manager.chromosomes:
            chromosome.evaluate(self.chromosome_manager.target_value)
        chromosome1, chromosome2 = self.chromosome_manager.do_roulette_wheel()
        self.chromosome_manager.crossover(chromosome1, chromosome2)
        was_matched = False
        for position in range(0, len(chromosome1.binary_string) + 1):
            binary_string1 = chromosome1.binary_string[:position] + chromosome2.binary_string[position:]
            binary_string2 = chromosome2.binary_string[:position] + chromosome1.binary_string[position:]
            if binary_string1 == chromosome1.binary_string and binary_string2 == chromosome2.binary_string:
                was_matched = True
        self.assertTrue(was_matched)

    def test_solve(self):
        chromosome, generation = self.chromosome_manager.solve()
        if chromosome.score == self.chromosome_manager.max_score:
            self.assertEqual(chromosome.result, self.chromosome_manager.target_value)
        else:
            self.assertEqual(generation, self.chromosome_manager.max_generations - 1)

    if __name__ == '__main__':
        unittest.main()
