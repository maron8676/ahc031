import getpass
import itertools
import math
import random
import sys


def li():
    return list(map(int, input().split()))


is_local = getpass.getuser() == "omotl"

W, D, N = li()
a = []
for d in range(D):
    a.append(li())

# determine rectangles
rect = [[] for _ in range(D)]
h = W // N
for d in range(D):
    for k in range(N):
        rect[d].append((k * h, 0, (k + 1) * h, W))

# output
for d in range(D):
    for k in range(N):
        i0, j0, i1, j1 = rect[d][k]
        print(i0, j0, i1, j1)
