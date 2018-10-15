from random import randint, random
from math import ceil
import csv
import timeit

test_suite_size = 5
mutation_rate = 0.05
sample_size = 500
number_ancestors = 10
number_iterations = 1000


class Test:
    def __init__(self, name, data):
        self.name = name
        self.data = data


# Helper function to generate an initial population from the test data sets
def generate_population(file_loc):
    population = []

    # Import the full data set.
    data_set = []
    with open(file_loc, 'r') as faultmatrixfile:
        csv_reader = csv.reader(faultmatrixfile, delimiter=',')
        for row in csv_reader:
            name = row[0]
            data = []
            for i in range(1, len(row)):
                data.append(int(row[i]))

            data_set.append(Test(name, data))

    # Take of random sample of size sample_size and append to the data set for sample_size counts
    # Special care has been taken to discard duplicates
    for i in range(sample_size):
        sample = []
        for j in range(test_suite_size):
            rand = randint(0, len(data_set) - 1)
            choice = data_set[rand]

            if choice not in sample:
                sample.append(choice)
            else:
                j -= 1

        if sample not in population:
            population.append(sample)
        else:
            i -= 1

    return population


# Evaluates a given test suite using APFD
def evaluate(test_suite):
    test_case_sum = 0
    faults_found = [0] * len(test_suite[0].data)

    for i in range(len(test_suite) - 1):
        for j in range(len(test_suite[i].data) - 1):
            if test_suite[i].data[j] == 1 and faults_found[j] == 0:
                test_case_sum += (i + 1)
                faults_found[j] = 1

    for i in range(len(faults_found) - 1):
        if faults_found[i] == 0:
            test_case_sum += (len(test_suite) + 1)

    return 1 - (test_case_sum / (len(test_suite) * len(test_suite[0].data))) + (1 / (2 * len(test_suite)))


# Cross-breeds ancestors to give a new population.
def crossbreed(ancestors, mutation_rate):
    pop = []
    for ancestor in ancestors:
        for other_ancestor in ancestors:
            if ancestor != other_ancestor:
                node_data = []
                for i in range(int(ceil(len(ancestor) / 2))):
                    node_data.append(ancestor[i])

                for test in other_ancestor:
                    if test not in node_data and len(node_data) < len(test.data):
                        node_data.append(test)

                to_add = node_data
                # Decide whether or not to mutate
                if random() < mutation_rate:
                    to_add = mutate(node_data)

                if to_add not in pop:
                    pop.append(to_add)

    return pop


# Helper function to mutate an ancestor before breeding
def mutate(test_suite):
    index_1 = randint(0, len(test_suite) - 1)
    index_2 = randint(0, len(test_suite) - 1)
    while index_1 == index_2:
        index_2 = randint(0, len(test_suite) - 1)

    buf = test_suite[index_1]
    test_suite[index_1] = test_suite[index_2]
    test_suite[index_2] = buf
    return test_suite


# Returns the best n candidates from a population (elitism strategy)
def get_best_n(population, number):
    return sorted(population, key=lambda x: evaluate(x), reverse=True)[:number]


def run():
    population = generate_population('src/FaultMatrixDataset_Small.csv')
    iterations = 0

    # Terminated by number of iterations, rather than optimal state or population convergence
    while iterations < number_iterations:
        ancestors = get_best_n(population, number_ancestors)
        population = crossbreed(ancestors, mutation_rate)
        iterations += 1

    best_suite = get_best_n(population, 1)[0]
    to_print = "Best suite was: "
    for i in range(len(best_suite)):
        to_print += best_suite[i].name + ','
    to_print = to_print[:-1]
    to_print += " with an APFD of " + str(evaluate(best_suite)) + " after " + str(iterations) + " iterations"
    print(to_print)


if __name__ == '__main__':
    for i in range(10):
        print("which took " + str(timeit.timeit(run, number=1)) + " seconds.")
