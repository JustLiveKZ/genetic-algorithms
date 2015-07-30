import math
import random
from chromosome import Chromosome


class ChromosomeManager(object):
    def __init__(self):
        self.target_value = 42
        self.crossover_rate = 0.7
        self.mutation_rate = 0.001
        self.max_generations = 20
        self.max_score = -1
        self.population = 10
        self.chromosome_lexeme_length = 9
        self.bits_in_lexeme = 4
        self.lexeme_number = 'number'
        self.lexeme_operator = 'operator'
        self.mappings = {
            '0000': 0,
            '0001': 1,
            '0010': 2,
            '0011': 3,
            '0100': 4,
            '0101': 5,
            '0110': 6,
            '0111': 7,
            '1000': 8,
            '1001': 9,
            '1010': lambda x, y: x + y,
            '1011': lambda x, y: x - y,
            '1100': lambda x, y: x * y,
            '1101': lambda x, y: x / y,
        }
        self.chromosomes = []

    def solve(self):
        self.generate_first_generation()
        for i in range(0, self.max_generations):
            for chromosome in self.chromosomes:
                chromosome.evaluate(self.target_value)
                if chromosome.score == self.max_score:
                    return chromosome
            chromosome1, chromosome2 = self.do_roulette_wheel()


    def generate_first_generation(self):
        for i in range(0, self.population):
            chromosome = Chromosome()
            chromosome.fitness_evaluator = self.get_default_fitness_evaluator()
            chromosome.fill_with_random_values()
            self.chromosomes.append(chromosome)

    def get_default_fitness_evaluator(self):
        def fitness_evaluator(_self, value, target_value):
            try:
                return 1 / math.fabs(value - target_value)
            except ZeroDivisionError:
                return self.max_score

        return fitness_evaluator

    def do_roulette_wheel(self):
        scores = [chromosome.score for chromosome in self.chromosomes]
        total_score = sum(scores)
        worth_of_one_point = 100 / total_score
        probabilities = [worth_of_one_point * score for score in scores]
        lucky_chromosomes = [None, None]
        for i in range(0, 2):
            random_number = random.randint(0, 100)
            index = 0
            probability = probabilities[index]
            while probability < random_number:
                index += 1
                probability += probabilities[index]
            lucky_chromosomes[i] = self.chromosomes[index]
        return tuple(lucky_chromosomes)


chromosome_manager = ChromosomeManager()
