from platypus import NSGAII, Problem, Generator, Solution
import random


class Customer:
    def __init__(self, weighting, requirements):
        self.weighting = weighting
        self.requirements = requirements


class Requirement:
    def __init__(self, value, cost):
        self.value = value
        self.cost = cost


class ReleaseProblem(Problem):
    def __init__(self, requirements):
        super(ReleaseProblem, self).__init__(1, 2)
        self.types = dict
        self.directions[0] = self.MAXIMIZE
        self.directions[1] = self.MINIMIZE

    def evaluate(self, solution):
        x = solution.variables
        print(x)
        solution.objectives[:] = solution.variables


class ReleaseGenerator(Generator):
    def __init__(self):
        super(ReleaseGenerator, self).__init__()

    def generate(self, problem):
        solution = Solution(Problem)
        var = []
        cost = 0
        while cost < problem.budget:
            # TODO: Get until would be larger than budget
        solution.variables = var



if __name__ == '__main__':
    # Get the customers and requirements from the files
    customers = []
    costs = []
    requirements = {}

    with open('test/classic-nrp/nrp1_customers') as customer_file:
        for line in customer_file:
            line_list = line.split()

            customers.append(Customer(int(line_list[0]), line_list[2:]))

    with open('test/classic-nrp/nrp1_requirements') as requirements_file:
        costs = requirements_file.readline().split()

    # Find the maximum value for customer weighting
    max_weight = -1
    for customer in customers:
        if customer.weighting > max_weight:
            max_weight = customer.weighting

    # Normalise the weighting for each customer
    for customer in customers:
        customer.weighting = customer.weighting / max_weight

    # Get a list of the value and cost of each requirement
    for i in range(1, len(costs)):
        value = 0

        for customer in customers:
            if str(i) in customer.requirements:
                value += customer.weighting * (1 / (customer.requirements.index(str(i)) + 1))

        requirements.update({str(i): [value, int(costs[i])]})

    print(requirements)

    problem = ReleaseProblem(requirements)
    alg = NSGAII(problem)
    alg.run(1)
