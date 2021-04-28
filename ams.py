import random
import time
from collections import Counter


def second_moment(seq):
    c = Counter(seq)
    return sum(v ** 2 for v in c.values())


if __name__ == '__main__':

    size = 1000000
    count_of_variables = 500
    variables = list(range(size))
    random.shuffle(variables)
    inds = sorted(variables[: count_of_variables])

    stream = []
    map = {}
    d = {}
    count = 0
    for x in range(size):
        c = random.randint(1, 1000)
        stream.append(c)
        count += 1
        if c not in map:
            map[c] = 0
        if c in d:
            map[c] += 1
        if count in inds and c not in d:
            d[c] = 0
        if c in d:
            d[c] += 1
        # if count % 1000 == 0:
        #     time.sleep(0.2)

    ams = int((len(stream) * sum((2 * v - 1) for v in d.values())) / len(d))

    print("0 moment: ", len(map))
    print("1st moment", size)
    print("2nd moment: ", second_moment(stream))
    print("2nd moment by ams for ", count_of_variables, " variables:", ams)
