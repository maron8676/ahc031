from collections import defaultdict, deque
from sys import stdin

readline = stdin.readline


def li():
    return list(map(int, readline().split()))


a = [48890,53150]
size = 350
limit = 129150

dp = [[False] * min(15, len(a) + 1) for _ in range(limit + 1)]
dp[0][0] = True

for i in range(1, len(dp[0])):
    aa = a[i - 1 + (len(a) + 1 - len(dp[0]))] // size * size
    if a[i - 1 + (len(a) + 1 - len(dp[0]))] % size > 0:
        aa += size
    for j in range(limit + 1):
        if dp[j][i - 1]:
            dp[j][i] = True
            if j + aa < limit + 1:
                dp[j + aa][i] = True

ans = 0
for i in range(limit, -1, -1):
    if dp[i][-1]:
        ans = i
        break
print(ans)

ans_list = []
for i in range(len(dp[0]) - 1, 0, -1):
    aa = a[len(a) + 1 - len(dp[0]) + i - 1] // size * size
    if a[len(a) + 1 - len(dp[0]) + i - 1] % size > 0:
        aa += size
    if ans - aa >= 0 and dp[ans - aa][i - 1]:
        ans_list.append(a[len(a) + 1 - len(dp[0]) + i - 1])
        ans -= aa
print(ans_list)
