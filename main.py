from manager import chromosome_manager

if __name__ == '__main__':
    chromosome = chromosome_manager.solve()

    print(chromosome.binary_string)
    print(chromosome.score)
