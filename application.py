from manager import chromosome_manager


class Application(object):
    def run(self):
        chromosome, generation = chromosome_manager.solve()
        if chromosome.score == chromosome_manager.max_score:
            print('Solution was found')
            print('Chromosome: %s' % chromosome)
            print('Generation: %s' % generation)
        else:
            print('Solution was not found')
            print('Below is nearest solution')
            print('Chromosome: %s' % chromosome)
            print('Result: %s' % chromosome.result)
            print('Score: %s' % chromosome.score)
            print('Generation: %s' % generation)
