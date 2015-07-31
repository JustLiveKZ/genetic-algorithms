import random
import math

import manager


class Chromosome(object):
    def __init__(self):
        self.binary_string = ''
        self.score = 0
        self.result = 0

    def __str__(self):
        return self.binary_string

    def evaluate_fitness(self, target_value):
        try:
            self.score = 1 / math.fabs(self.result - target_value)
        except ZeroDivisionError:
            self.score = manager.chromosome_manager.max_score

    def evaluate(self, target_value):
        awaiting_lexeme = manager.chromosome_manager.lexeme_number
        awaiting_operator = None
        for i in range(0, manager.chromosome_manager.chromosome_lexeme_length):
            lexeme_code = self.binary_string[i * manager.chromosome_manager.bits_in_lexeme: (i + 1) * manager.chromosome_manager.bits_in_lexeme]
            if lexeme_code in manager.chromosome_manager.mappings:
                lexeme = manager.chromosome_manager.mappings[lexeme_code]
                if isinstance(lexeme, int) and awaiting_lexeme == manager.chromosome_manager.lexeme_number:
                    if awaiting_operator:
                        try:
                            self.result = awaiting_operator(self.result, lexeme)
                        except ZeroDivisionError:
                            pass
                    else:
                        self.result = lexeme
                    awaiting_lexeme = manager.chromosome_manager.lexeme_operator
                elif hasattr(lexeme, '__call__') and awaiting_lexeme == manager.chromosome_manager.lexeme_operator:
                    awaiting_operator = lexeme
                    awaiting_lexeme = manager.chromosome_manager.lexeme_number
        self.evaluate_fitness(target_value)

    def fill_with_random_values(self):
        for i in range(manager.chromosome_manager.chromosome_lexeme_length * manager.chromosome_manager.bits_in_lexeme):
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
