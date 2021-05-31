import random

from math import sqrt

alphabet = ['a', 'b', 'c', 'd']
def generate_regex(max_len = 100, i = 1):
    if i > max_len:
        return random.choice(alphabet)
    op = random.choices(population=[1,2,3,4], weights=[0.15, 0.15, 0.5, 0.2], k=1)[0]

    if op == 1:
        return generate_regex(max_len, i+1) + "*"
    elif op == 2:
        return generate_regex(max_len, i*2) + "|" + generate_regex(max_len, i*2)
    elif op == 3:
        return generate_regex(max_len, i*2) + generate_regex(max_len, i*2)
    else:
        return "(" + generate_regex(max_len, i+1) + ")"

for i in range(1, 10):
    with open("random_file" + str(i) + ".in", "w") as fout:
        fout.write(generate_regex(3*i*int(sqrt(i)) + 2))
