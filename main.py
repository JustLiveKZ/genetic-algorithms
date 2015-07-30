from manager import chromosome_manager

if __name__ == '__main__':
    chromosome, generation = chromosome_manager.solve()

    print(chromosome.binary_string)
    print(chromosome.result)
    print(chromosome.score)
    print(generation)
