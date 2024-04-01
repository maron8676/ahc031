import statistics
from collections import defaultdict, deque
from sys import stdin

readline = stdin.readline


def li():
    return list(map(int, readline().split()))


score_list = []
with open("latest.txt", mode="r", encoding="utf8") as f:
    for line in f:
        score_list.append(int(line))

grid = [[[] for _ in range(5)] for _ in range(5)]
for i in range(1000):
    with open(f"in/{i:04}.txt", mode="r", encoding="utf8") as f:
        line = f.readline()
        params = list(map(int, line.split()))
        D = params[1]
        N = params[2]

        d_index = min(D // 10, 4)
        n_index = min(N // 10, 4)

        grid[d_index][n_index].append(score_list[i])

score_grid = [[0] * 5 for _ in range(5)]
for i in range(5):
    for j in range(5):
        score_grid[i][j] = round(statistics.mean(grid[i][j]))

for row in score_grid:
    print(*row)
