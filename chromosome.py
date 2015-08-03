import random
import math


class Chromosome(object):
    def __init__(self, manager):
        self.binary_string = ''
        self.score = 0
        self.result = 0
        self.manager = manager

    def __str__(self):
        return self.binary_string

    def evaluate_fitness(self, target_value):
        try:
            self.score = 1 / math.fabs(self.result - target_value)
        except ZeroDivisionError:
            self.score = self.manager.max_score

    def evaluate(self, target_value):
        awaiting_lexeme = self.manager.LEXEME_TYPE_NUMBER
        awaiting_operator = None
        for i in range(0, self.manager.chromosome_length_in_lexemes):
            lexeme_code = self.binary_string[i * self.manager.lexeme_length_in_bits: (i + 1) * self.manager.lexeme_length_in_bits]
            if lexeme_code in self.manager.mappings:
                lexeme = self.manager.mappings[lexeme_code]
                if isinstance(lexeme, int) and awaiting_lexeme == self.manager.LEXEME_TYPE_NUMBER:
                    if awaiting_operator:
                        try:
                            self.result = awaiting_operator(self.result, lexeme)
                        except ZeroDivisionError:
                            pass
                    else:
                        self.result = lexeme
                    awaiting_lexeme = self.manager.LEXEME_TYPE_OPERATOR
                elif hasattr(lexeme, '__call__') and awaiting_lexeme == self.manager.LEXEME_TYPE_OPERATOR:
                    awaiting_operator = lexeme
                    awaiting_lexeme = self.manager.LEXEME_TYPE_NUMBER
        self.evaluate_fitness(target_value)

    def fill_with_random_values(self):
        for i in range(self.manager.chromosome_length_in_lexemes * self.manager.lexeme_length_in_bits):
            self.binary_string += str(random.randint(0, 1))

    def mutate(self, mutation_rate):
        mutated_chars_count = 0
        for i in range(0, len(self.binary_string)):
            if random.random() < mutation_rate:
                mutated_chars_count += 1
                if self.binary_string[i] == '1':
                    self.binary_string = self.binary_string[:i] + '0' + self.binary_string[i + 1:]
                else:
                    self.binary_string = self.binary_string[:i] + '1' + self.binary_string[i + 1:]
        return mutated_chars_count
