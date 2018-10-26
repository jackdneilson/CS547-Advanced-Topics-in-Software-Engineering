from platypus import NSGAII, Problem, Generator, Solution, Real, Mutation
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
        super(ReleaseProblem, self).__init__(1, 2)
        self.genepool = requirements
        self.budget = budget
        self.initial_size = 50
        self.types = [Real(0, 50), Real(0, 50)]
        self.directions[0] = self.MAXIMIZE
        self.directions[1] = self.MINIMIZE

    def evaluate(self, solution):
        sum_value = 0
        sum_cost = 0

        for requirement in solution.variables[0]:
            sum_value += requirement.value
            sum_cost += requirement.cost

        solution.objectives[:] = [sum_value, sum_cost]
        solution.evaluated = True
        return [sum_value, sum_cost]


class ReleaseGenerator(Generator):
    def __init__(self):
        super(ReleaseGenerator, self).__init__()

    def generate(self, problem):
        solution = Solution(problem)

        solution_vars = []
        for i in range(problem.initial_size):
            node = []
            generated = False
            while not generated:
                rand = random.randint(0, len(problem.genepool) - 1)
                choice = problem.genepool[rand]

                if choice not in node:
                    if get_cost(node) + choice.cost > problem.budget:
                        generated = True
                    else:
                        node.append(choice)

            solution_vars.append(node)

        solution.variables = solution_vars
        return solution


class ReleaseMutator(Mutation):
    def __init__(self, probability=1, distribution_index=20.0):
        super(ReleaseMutator, self).__init__()
        self.probability = probability
        self.distribution_index = distribution_index

    def mutate(self, parent):
        child = copy.deepcopy(parent)
        problem = child.problem
        probability = self.probability

        if isinstance(probability, int):
            probability /= float(len([t for t in problem.types if isinstance(t, Real)]))

        # TODO: Mutation happens here
        for i in range(len(child.variables)):
            if isinstance(problem.types[i], Real):
                if random.uniform(0.0, 1.0) <= probability:
                    child.variables[i] = self.pm_mutation(float(child.variables[i]),
                                                          problem.types[i].min_value,
                                                          problem.types[i].max_value)

        # TODO: Mutation happens here

        child.evaluated = False
        return child



def get_cost(node):
    cost = 0
    for req in node:
        cost += req.cost

    return cost

if __name__ == '__main__':
    # Get the customers and requirements from the files
    customers = []
    costs = []
    requirements = []

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

    problem = ReleaseProblem(requirements, 50)
    alg = NSGAII(problem, generator=ReleaseGenerator())
    alg.run(5000)
    for requirement in alg.result[0].variables[0]:
        print("id: " + str(requirement.id))
        print("value:" + str(requirement.value))
        print("cost: " + str(requirement.cost))
