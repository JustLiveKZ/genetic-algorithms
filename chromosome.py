import random

from manager import chromosome_manager


class Chromosome(object):
    def __init__(self):
        self.binary_string = ''
        self.score = 0
        self.fitness_evaluator = None

    def evaluate(self, target_value):
        result = 0
        awaiting_lexeme = chromosome_manager.lexeme_number
        awaiting_operator = None
        for i in range(0, chromosome_manager.chromosome_lexeme_length):
            lexeme_code = self.binary_string[i * chromosome_manager.bits_in_lexeme: (i + 1) * chromosome_manager.bits_in_lexeme]
            if lexeme_code in chromosome_manager.mappings:
                lexeme = chromosome_manager.mappings[lexeme_code]
                if isinstance(lexeme, int) and awaiting_lexeme == chromosome_manager.lexeme_number:
                    if awaiting_operator:
                        result = awaiting_operator(result, lexeme)
                    else:
                        result = lexeme
                    awaiting_lexeme = chromosome_manager.lexeme_number
                elif hasattr(lexeme, '__call__') and awaiting_lexeme == chromosome_manager.lexeme_operator:
                    awaiting_operator = lexeme
                    awaiting_lexeme = chromosome_manager.lexeme_number
        self.score = self.fitness_evaluator(result, target_value)

    def fill_with_random_values(self):
        for i in range(chromosome_manager.chromosome_lexeme_length * chromosome_manager.bits_in_lexeme):
            self.binary_string += str(random.randint(0, 1))
