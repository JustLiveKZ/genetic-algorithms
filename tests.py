import unittest

from chromosome import Chromosome
from manager import ChromosomeManager


class ChromosomeTestCase(unittest.TestCase):
    chromosome = None

    def setUp(self):
        self.chromosome = Chromosome()

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

    def test_fill_with_random_values(self):
        self.chromosome.fill_with_random_values()
        self.assertEqual(len(self.chromosome.binary_string), 36)
        for char in self.chromosome.binary_string:
            self.assertTrue(0 <= int(char) <= 1)


class ChromosomeManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.chromosome_manager = ChromosomeManager()

    def test_generate_first_generation(self):
        self.chromosome_manager.generate_first_generation()
        self.assertEqual(len(self.chromosome_manager.chromosomes), 10)

    def test_get_index(self):
        probabilities = [10, 5, 10, 20, 50, 5]
        self.assertEqual(self.chromosome_manager.get_index(7, probabilities), 0)
        self.assertEqual(self.chromosome_manager.get_index(10, probabilities), 0)
        self.assertEqual(self.chromosome_manager.get_index(11, probabilities), 1)
        self.assertEqual(self.chromosome_manager.get_index(25, probabilities), 2)
        self.assertEqual(self.chromosome_manager.get_index(38, probabilities), 3)
        self.assertEqual(self.chromosome_manager.get_index(73, probabilities), 4)
        self.assertEqual(self.chromosome_manager.get_index(96, probabilities), 5)
        self.assertEqual(self.chromosome_manager.get_index(100, probabilities), 5)

    def test_roulette_wheel(self):
        self.chromosome_manager.generate_first_generation()
        for chromosome in self.chromosome_manager.chromosomes:
            chromosome.evaluate(self.chromosome_manager.target_value)
        chromosome1, chromosome2 = self.chromosome_manager.do_roulette_wheel()
        self.assertNotEqual(chromosome1, chromosome2)
        self.assertIn(chromosome1, self.chromosome_manager.chromosomes)
        self.assertIn(chromosome2, self.chromosome_manager.chromosomes)


if __name__ == '__main__':
    unittest.main()
