from random import randint

goal_string = "Hello World!"
possible_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !"

# Function to generate a random string of given length
def random_string(possible_chars, length):
    ret = ""
    for i in range(length):
        rand = randint(0, len(possible_chars) -1)
        ret += possible_chars[rand]
    return ret


cur_string = ""
attempts = 0

# Search for the goal string by repeatedly generating random strings
while cur_string != goal_string:
    cur_string = random_string(possible_chars, len(goal_string))
    print(cur_string)
    attempts += 1

print(attempts)
