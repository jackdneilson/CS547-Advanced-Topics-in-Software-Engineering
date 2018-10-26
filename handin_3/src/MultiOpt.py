from platypus import NSGAII, Problem, Integer
from matplotlib import pyplot as plt
import copy
import random


class Customer:
    def __init__(self, weighting, requirements):
        self.weighting = weighting
        self.requirements = requirements


class Requirement:
    def __init__(self, id, value, cost):
        self.id = id
        self.value = value
        self.cost = cost


class ReleaseProblem(Problem):
    def __init__(self, requirements, budget):
        super(ReleaseProblem, self).__init__(len(requirements), 2)
        self.requirements = requirements
        self.budget = budget
        self.types[:] = Integer(0,1)
        self.directions[0] = self.MAXIMIZE
        self.directions[1] = self.MINIMIZE

    # Sum the value and cost using list lookup
    def evaluate(self, solution):
        sum_value = 0
        sum_cost = 0

        for i in range(len(solution.variables) - 1):
            if solution.variables[i] == 1:
                sum_value += solution.problem.requirements[i].value
                sum_cost += solution.problem.requirements[i].cost

        if sum_cost > self.budget:
            sum_value = -1

        solution.objectives[:] = [sum_value, sum_cost]
        solution.evaluated = True
        #return [sum_value, sum_cost]


if __name__ == '__main__':
    # Get the customers and requirements from the files
    customers = []
    costs = []
    requirements = []

    budget = 120

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

        requirements.append(Requirement(i, value, int(costs[i])))

    # Instantiate the problem and run, then print the results
    problem = ReleaseProblem(requirements, 0.5 * sum(req.cost for req in requirements))
    alg = NSGAII(problem)
    alg.run(10000)
    for result in alg.result:
        print(result.objectives)

    plt.scatter([s.objectives[0] for s in alg.result],
                [s.objectives[1] for s in alg.result])
    plt.xlim([min(s.objectives[0] for s in alg.result), max(s.objectives[0] for s in alg.result)])
    plt.ylim([min(s.objectives[1] for s in alg.result), max(s.objectives[1] for s in alg.result)])
    plt.show()
