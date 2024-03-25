import getpass
import itertools
import math
import random
import sys


def li():
    return list(map(int, input().split()))


is_local = getpass.getuser() == "omotl"

W, D, N = li()
a_list = []
for d in range(D):
    a_list.append(li())

# determine rectangles
rect = [[] for _ in range(D)]
for d in range(D):
    a = a_list[d]
    a.sort(reverse=True)
    remain = W
    upper = 0
    for k in range(N):
        h = a[k] // W
        if a[k] % W != 0:
            h += 1
        h = min(h, remain - (N - 1 - k))
        rect[d].insert(0, (upper, 0, upper + h, W))
        upper += h
        remain -= h

# output
for d in range(D):
    for k in range(N):
        i0, j0, i1, j1 = rect[d][k]
        print(i0, j0, i1, j1)
