import random

import chromosome as chromosome_module

DEFAULT_CROSSOVER_RATE = 0.7
DEFAULT_MUTATION_RATE = 0.001
DEFAULT_MAX_GENERATIONS = 1000
DEFAULT_MAX_SCORE = 1e18
DEFAULT_POPULATION = 10
DEFAULT_CHROMOSOME_LENGTH_IN_LEXEMES = 9


class ChromosomeManager(object):
    (LEXEME_TYPE_NUMBER, LEXEME_TYPE_OPERATOR) = range(0, 2)

    def __init__(self, target_value, crossover_rate=DEFAULT_CROSSOVER_RATE, mutation_rate=DEFAULT_MUTATION_RATE,
                 max_generations=DEFAULT_MAX_GENERATIONS, max_score=DEFAULT_MAX_SCORE,
                 population=DEFAULT_POPULATION, chromosome_length_in_lexemes=DEFAULT_CHROMOSOME_LENGTH_IN_LEXEMES):
        self.target_value = target_value
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.max_score = max_score
        self.population = population
        self.chromosome_length_in_lexemes = chromosome_length_in_lexemes
        self.lexeme_length_in_bits = 4
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
        for generation in range(0, self.max_generations):
            for chromosome in self.chromosomes:
                chromosome.evaluate(self.target_value)
                if chromosome.score == self.max_score:
                    return chromosome, generation
            new_generation = []
            while len(new_generation) != self.population:
                chromosome1, chromosome2 = self.do_roulette_wheel()
                self.crossover(chromosome1, chromosome2)
                chromosome1.mutate(self.mutation_rate)
                chromosome2.mutate(self.mutation_rate)
                new_generation.append(chromosome1)
                new_generation.append(chromosome2)
            self.chromosomes = new_generation
        chromosome = max(self.chromosomes, key=lambda c: c.score)
        return chromosome, self.max_generations - 1

    def generate_first_generation(self):
        for i in range(0, self.population):
            chromosome = chromosome_module.Chromosome(self)
            chromosome.fill_with_random_values()
            self.chromosomes.append(chromosome)

    def do_roulette_wheel(self):
        scores = [chromosome.score for chromosome in self.chromosomes]
        total_score = sum(scores)
        worth_of_one_point = 1. / total_score
        probabilities = [worth_of_one_point * score for score in scores]
        try:
            assert sum(probabilities) == 1.
        except AssertionError:
            probabilities[-1] = 1. - sum(probabilities[:-1])
            assert sum(probabilities) == 1.
        lucky_chromosomes = []
        for i in range(0, 2):
            while True:
                random_number = random.random()
                index = self.get_index(random_number, probabilities)
                if self.chromosomes[index] not in lucky_chromosomes:
                    break
            lucky_chromosomes.append(self.chromosomes[index])
        return tuple(lucky_chromosomes)

    def get_index(self, random_number, probabilities):
        index = 0
        probability = probabilities[index]
        while probability < random_number:
            index += 1
            probability += probabilities[index]
        return index

    def crossover(self, chromosome1, chromosome2):
        if random.random() < self.crossover_rate:
            position = random.randint(0, self.chromosome_length_in_lexemes * self.lexeme_length_in_bits - 1)
            temp = chromosome1.binary_string[position:]
            chromosome1.binary_string = chromosome1.binary_string[:position] + chromosome2.binary_string[position:]
            chromosome2.binary_string = chromosome2.binary_string[:position] + temp
