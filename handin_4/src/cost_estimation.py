from deap import base, creator, gp, tools, algorithms
from enum import Enum
import math
import operator
import sys
import numpy
from sklearn import model_selection
from sklearn import metrics
from sklearn.linear_model import LinearRegression


# Does not allow for dividebyzero exceptions
def protected_div(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1


class EvalMethods(Enum):
    MEAN_ABSOLUTE_ERROR = 1
    ROOT_MEAN_SQUARED_ERROR = 2


if __name__ == '__main__':
    # First attempt solution using genetic programming
    # Choose evaluation method
    evaluation_method = EvalMethods.ROOT_MEAN_SQUARED_ERROR
    min_tree_depth = 3
    max_tree_depth = 5
    number_splits = 10

    input_names = []
    input_sets = []
    actual_costs = []

    # Import the data file
    with open(sys.argv[1]) as data:
        for line in data:
            if line[0] != "%" and line[0:9] != "@relation" and line[0:5] != "@data" and line != "\n":
                if line[0:10] == "@attribute":
                    if line.split()[1] != "Effort" and line.split()[1] != "EffortMM" and line.split()[1] != "MM":
                        input_names.append(line.split()[1])
                else:
                    new_inputs = line.split(',')[:-1]
                    for i in range(len(new_inputs)):
                        new_inputs[i] = float(new_inputs[i])
                    input_sets.append(new_inputs)
                    actual_costs.append(float(line.split(',')[-1:][0].split('\n')[0]))

    number_inputs = len(input_names)
    max_cost = max(actual_costs)
    min_cost = min(actual_costs)

    # Generate a set of primitives to allow for generation / permutation
    prim_set = gp.PrimitiveSet("MAIN", number_inputs)
    prim_set.addPrimitive(operator.add, 2)
    prim_set.addPrimitive(operator.sub, 2)
    prim_set.addPrimitive(operator.mul, 2)
    prim_set.addPrimitive(protected_div, 2)
    prim_set.addPrimitive(operator.neg, 1)
    prim_set.addPrimitive(math.cos, 1)
    prim_set.addPrimitive(math.sin, 1)

    # Define a fitness object to evaluate potential solutions (weight is -1.0 as we are trying to minimise)
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

    # Define an individual in the population (in this case a primitive tree)
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

    # Register the expressions defined, create an individual creation function,
    # create a population creation function, and register a compilation function
    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genFull, pset=prim_set, min_=3, max_=15)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=prim_set)

    # Define an evaluation function
    def evaluate_soln(input_sets, actual_costs, node):
        # Compile the tree into a runnable program
        func = toolbox.compile(expr=node)

        if evaluation_method == EvalMethods.MEAN_ABSOLUTE_ERROR:
            sae = 0
            for i, input_set in enumerate(input_sets):
                sae += abs(actual_costs[i] - func(*input_set))
            return [sae / len(input_sets)]

        elif evaluation_method == EvalMethods.ROOT_MEAN_SQUARED_ERROR:
            sumsq = 0
            for i, input_set in enumerate(input_sets):
                sumsq += math.pow((actual_costs[i] - func(*input_set)), 2)
            return [math.sqrt(sumsq / len(input_sets))]

    # Split the data into training and testing sets
    for train_indices, test_indices in model_selection.KFold(number_splits).split(input_sets):
        input_set_train = []
        input_set_test = []
        cost_train = []
        cost_test = []

        for index in train_indices:
            input_set_train.append(input_sets[index])
            cost_train.append(actual_costs[index])
        for index in test_indices:
            input_set_test.append(input_sets[index])
            cost_test.append(actual_costs[index])

        # Register the evaluation function, the selection function, the mating operation, and the mutation operation
        toolbox.register("evaluate", evaluate_soln, input_set_train, cost_train)
        toolbox.register("select", tools.selTournament, tournsize=(math.floor(len(input_set_train) / 2)))

        toolbox.register("mate", gp.cxOnePoint)
        toolbox.register("expr_mut", gp.genFull, min_=0, max_=4)
        toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=prim_set)

        # Decorate the mating and mutation operations to limit height of generated individuals (prevents bloat)
        toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
        toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

        # Declare some statistics to evaluate genetic programming against other methods
        stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
        stats_size = tools.Statistics(len)
        mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
        mstats.register("avg", numpy.mean)
        mstats.register("std", numpy.std)
        mstats.register("min", numpy.min)
        mstats.register("max", numpy.max)

        # Run the algorithm and take the best generated solution
        pop = toolbox.population(n=100)
        hof = tools.HallOfFame(1)
        algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 1000, stats=mstats, halloffame=hof, verbose=False)
        print(evaluate_soln(input_set_test, cost_test, hof[0]))

        # Attempt solution using linear regression
        # Create a model
        lnr = LinearRegression()
        lnr.fit(input_set_train, cost_train)

        # Use the model to predict cost
        lnr_pred = lnr.predict(input_set_test)

        if evaluation_method == EvalMethods.MEAN_ABSOLUTE_ERROR:
            print(metrics.mean_absolute_error(cost_test, lnr_pred))
        elif evaluation_method == EvalMethods.ROOT_MEAN_SQUARED_ERROR:
            print(math.sqrt(metrics.mean_squared_error(cost_test, lnr_pred)))
