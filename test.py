from math import sqrt

def func(i):
    print("func called with i =", i)

ar = []
for i in range(10):
    ar.append(lambda i = i: func(i))

for f in ar:
    f()