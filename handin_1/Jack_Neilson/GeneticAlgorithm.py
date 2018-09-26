from random import randint

population_size = 50
ancestor_count = 10
goal_string = "Hello World!"
possible_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !"
mutation_chance_percentage = 5


# Fitness function for given node in population
def evaluate(node):
    matching_chars = 0
    for i in range(len(node)):
        if node[i] == goal_string[i]:
            matching_chars += 1
    return matching_chars


# Function to find matching string using GA
def find_match(pop, goal):
    iterations = 0

    # Loop until goal string is found
    while True:
        # Evaluate current population
        for cur_node in pop.keys():
            pop[cur_node] = evaluate(cur_node)

        # Check for match
        for cur_node, fitness in pop.items():
            if fitness == len(goal):
                return iterations

        # Get best ancestors to generate next population
        ancestors = sorted(pop.items(), key=lambda x: x[1], reverse=True)[:ancestor_count]
        print(ancestors[0])
        ancestors = dict(ancestors)

        # Decide whether or not to mutate
        to_remove = []
        to_add = []
        for cur_node, fitness in ancestors.items():
            mutate = randint(1, 100)
            if mutate <= mutation_chance_percentage:
                rand_char = possible_chars[randint(0, len(possible_chars) - 1)]
                rand_index = randint(0, len(cur_node) - 1)
                replace_string = list(cur_node)
                replace_string[rand_index] = rand_char
                to_remove.append(cur_node)
                to_add.append("".join(replace_string))

        for node in to_remove:
            ancestors.pop(node)

        for node in to_add:
            ancestors[node] = -1

        # Cross-breed best ancestors
        pop = {}
        for cur_node in ancestors.keys():
            for breed_node in ancestors.keys():
                if not cur_node == breed_node:
                    new_node = cur_node[:6] + breed_node[6:]
                    pop[new_node] = -1

        iterations += 1


if __name__ == '__main__':
    # Initialise population as an empty dict
    population = {}

    # Generate the population randomly from possible characters
    for i in range(population_size):
        string = ""

        for j in range(len(goal_string)):
            rand = randint(0, len(possible_chars) - 1)
            string += possible_chars[rand]

        population[string] = -1

    print(find_match(population, goal_string))
