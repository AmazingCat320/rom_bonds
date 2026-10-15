import random as rn

stuff = "1234567"

print(stuff[-3:])


class get_wait_time:
    def __init__(self):
        pass
    
    def fast_wait(self):
        x = rn.uniform(2, 5)
        return x

    def slow_wait(self):
        x = rn.uniform(5, 8)
        return x
    
j = 1
average = 0
n = 67
wait_time = get_wait_time()
for i in range(n):
    if j <= 3:
        x = wait_time.fast_wait()
        j += 1
    elif j > 3 and j <= 6:
        x = wait_time.slow_wait()
        j += 1
    if j > 6:
        j = 1
    average += x
    print(x)

print("avg: ", average/n)

average = 0
def wait():
    lo, hi = rn.choice([(2, 6), (7, 10)])
    return rn.uniform(lo, hi)

for i in range(n):
    x = wait()
    print(x)
    average += x

print("avg: ", average/n)