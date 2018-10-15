import csv
import timeit
from random import randint
test_suite_size = 5


class Test:
    def __init__(self, name, data):
        self.name = name
        self.data = data


# Helper function to generate a random starting node
def get_data_set(file_loc):
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

    return data_set


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


# Generates a random node from the data set
def generate_random_node(data_set):
    test_suite = []
    for i in range(test_suite_size):
        test_suite.append(data_set[randint(0, len(data_set) - 1)])

    return test_suite


def run():
    data_set = get_data_set('src/FaultMatrixDataset_Small.csv')

    max_found = generate_random_node(data_set)
    APFD = evaluate(max_found)
    for i in range(1000000 - 1):
        node = generate_random_node(data_set)
        APFD += evaluate(node)
        if evaluate(max_found) < evaluate(node):
            max_found = node

    print("Best found was: " + str(evaluate(max_found)) + ", avg was " + str(APFD / 1000000))


if __name__ == '__main__':
    print("which took " + str(timeit.timeit(run, number=1)) + " seconds.")
