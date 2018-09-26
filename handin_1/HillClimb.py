goal_string = "Hello World!"
possible_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !"


# Evaluate a given node
def evaluate(node):
    matching_chars = 0
    for i in range(len(node)):
        if node[i] == goal_string[i]:
            matching_chars += 1
    return matching_chars


# Find a route from a starting string to a goal string
def find_match(start_point, end_point):
    cur_iter = start_point
    pos = 0
    attempts = 0

    # While the current iteration is not at the endpoint continue searching
    while cur_iter != end_point:
        try:
            # Move a cursor forward while the current iteration matches the goal string
            while cur_iter[pos] == end_point[pos]:
                pos += 1
                if pos == len(goal_string):
                    return attempts
        except IndexError:
            cur_iter += " "

        # Generate a dict of adjacent nodes and evaluate
        adjacent_nodes = {}

        for i in range(len(possible_chars)):
            to_insert = cur_iter[:pos] + possible_chars[i]
            adjacent_nodes[to_insert] = evaluate(to_insert)

        # Take the best out of the possible adjacent nodes and move to that
        cur_iter = sorted(adjacent_nodes.items(), key=lambda x: x[1], reverse=True)[:1][0][0]

        attempts += 1
    return attempts


if __name__ == '__main__':
    print("Attempts: " + str(find_match("Hello! This is a test.", goal_string)))
