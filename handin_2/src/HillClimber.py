import csv
import timeit
from random import randint

test_suite_size = 5


class Test:
    def __init__(self, name, data):
        self.name = name
        self.data = data


# Helper function to generate a random starting node
def generate_random_node(file_loc):
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

    test_suite = []
    for i in range(test_suite_size):
        test_suite.append(data_set[randint(0, len(data_set) - 1)])

    return test_suite


# Gives the neighbours of a test suite
def generate_neighbours(test_suite):
    neighbours = []
    for i in range(len(test_suite) - 1):
        cur_neighbour = []
        cur_neighbour += test_suite[:i]
        cur_neighbour += test_suite[i + 1: i + 2]
        cur_neighbour += test_suite[i: i + 1]
        cur_neighbour += test_suite[i + 2:]

        neighbours.append(cur_neighbour)
    return neighbours


# Finds the best test suite from a list of test suites
def find_best(test_suites):
    return sorted(test_suites, key=lambda x: evaluate(x), reverse=True)[:1][0]


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


def run():
    cur_node = generate_random_node('src/FaultMatrixDataset_Large.csv')
    while True:
        neighbours = generate_neighbours(cur_node)

        if evaluate(find_best(neighbours)) <= evaluate(cur_node):
            print("Maximum found, APFD: " + str(evaluate(cur_node)))
            break
        else:
            cur_node = find_best(neighbours)


if __name__ == '__main__':
    for i in range(10):
        print("which took " + str(timeit.timeit(run, number=1)) + " seconds.")
