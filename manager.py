import random

import chromosome as chromosome_module


class ChromosomeManager(object):
    def __init__(self):
        self.target_value = 42
        self.crossover_rate = 0.7
        self.mutation_rate = 0.001
        self.max_generations = 1000
        self.max_score = 1e18
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
            chromosome = chromosome_module.Chromosome()
            chromosome.fill_with_random_values()
            self.chromosomes.append(chromosome)

    def do_roulette_wheel(self):
        scores = [chromosome.score for chromosome in self.chromosomes]
        total_score = sum(scores)
        worth_of_one_point = 100 / total_score
        probabilities = [worth_of_one_point * score for score in scores]
        lucky_chromosomes = [None, None]
        for i in range(0, 2):
            while True:
                random_number = random.randint(1, 100)
                index = self.get_index(random_number, probabilities)
                if self.chromosomes[index] not in lucky_chromosomes:
                    break
            lucky_chromosomes[i] = self.chromosomes[index]
        return tuple(lucky_chromosomes)

    def get_index(self, random_number, probabilities):
        index = 0
        probability = probabilities[index]
        while probability < random_number:
            index += 1
            if index == len(probabilities):
                index -= 1
                break
            probability += probabilities[index]
        return index

    def crossover(self, chromosome1, chromosome2):
        if random.random() < self.crossover_rate:
            position = random.randint(0, self.chromosome_lexeme_length * self.bits_in_lexeme)
            temp = chromosome1.binary_string[position:]
            chromosome1.binary_string = chromosome1.binary_string[:position] + chromosome2.binary_string[position:]
            chromosome2.binary_string = chromosome2.binary_string[:position] + temp


chromosome_manager = ChromosomeManager()
