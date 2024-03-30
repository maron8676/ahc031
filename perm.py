import getpass
import math
import random
import sys
from collections import defaultdict


def li():
    return list(map(int, input().split()))


def calc_cost(D, N, a_list, rects_list):
    # 重なりがないことを確認
    for d in range(D):
        rects = rects_list[d]
        for i in range(N - 1):
            rect1 = rects[i]
            for j in range(i + 1, N):
                rect2 = rects[j]
                if rect1[0] < rect2[0] < rect1[2] and rect1[1] < rect2[1] < rect1[3]:
                    return -1
                if rect1[0] < rect2[2] < rect1[2] and rect1[1] < rect2[3] < rect1[3]:
                    return -1

    cost = 0

    h_set = set()
    v_set = set()
    for d in range(D):
        # 広さ足りない分
        a = a_list[d]
        rects = rects_list[d]
        for i in range(N):
            rect = rects[i]
            area = (rect[2] - rect[0]) * (rect[3] - rect[1])
            cost += max(0, a[i] - area) * 100

        # 壁作成と撤去
        h_set_next = set()
        v_set_next = set()
        rects = rects_list[d]
        for rect in rects:
            if 0 < rect[0] < W:
                for i in range(rect[1], rect[3]):
                    h_set_next.add((rect[0] - 1) * W + i)
            if 0 < rect[2] < W:
                for i in range(rect[1], rect[3]):
                    h_set_next.add((rect[2] - 1) * W + i)

            if 0 < rect[1] < W:
                for i in range(rect[0], rect[2]):
                    v_set_next.add(i * W + rect[1])
            if 0 < rect[3] < W:
                for i in range(rect[0], rect[2]):
                    v_set_next.add(i * W + rect[3])

        if d != 0:
            cost += len(h_set_next - h_set)
            cost += len(h_set - h_set_next)
            cost += len(v_set_next - v_set)
            cost += len(v_set - v_set_next)

        h_set = h_set_next
        v_set = v_set_next

    print(cost, file=sys.stderr)


is_local = getpass.getuser() == "omotl"

W, D, N = li()
a_list = []
for d in range(D):
    a_list.append(li())

a_sum_list = []
a2_list = []
for d in range(D):
    base = 1
    a_sum = 0
    a2 = []
    for n in range(N):
        a = a_list[d][n] // (W // base)
        if a_list[d][n] % (W // base) > 0:
            a += 1
        a2.append([a * (W // base)])
        a_sum += a * (W // base)
    a2_list.append(a2)
    a_sum_list.append(a_sum)

print(a2_list)

max_a_list = []
for n in range(N):
    max_a = 0
    for d in range(D):
        if max_a < sum(a2_list[d][n]):
            max_a = sum(a2_list[d][n])
    max_a_list.append(max_a)
print(max_a_list)
best_a = a2_list
best_score = sum(max_a_list)
best_swap = N * 2
print(best_score)

# ランダムなdとnを決める
# 要素があればランダムに1つ取り出す
for t2 in range(10):
    a2_list = []
    for d in range(D):
        base = 1
        a_sum = 0
        a2 = []
        for n in range(N):
            a = a_list[d][n] // (W // base)
            if a_list[d][n] % (W // base) > 0:
                a += 1
            a2.append([a * (W // base)])
            a_sum += a * (W // base)
        a2_list.append(a2)
    max_a_list = []
    for n in range(N):
        max_a = 0
        for d in range(D):
            if max_a < sum(a2_list[d][n]):
                max_a = sum(a2_list[d][n])
        max_a_list.append(max_a)
    print(max_a_list)
    best_score = sum(max_a_list)
    print(best_score)

    for t1 in range(1000):
        i = random.randint(0, N - 1)
        d = -1
        sum_max = -1
        for dd in range(D):
            if sum_max < sum(a2_list[dd][i]):
                sum_max = sum(a2_list[dd][i])
                d = dd
        if len(a2_list[d][i]) == 0:
            continue
        # print(a2_list)
        j = random.randint(0, N - 1)
        ope_type = 0
        if random.random() < 0.8:
            ope_type = 1
            index = random.randint(0, len(a2_list[d][i]) - 1)
            a = a2_list[d][i].pop(index)
            a2_list[d][j].append(a)
        else:
            ope_type = 2
            a = a2_list[d][i]
            a2_list[d][i] = a2_list[d][j]
            a2_list[d][j] = a
        # print(d, i, j)

        max_a_list = []
        for n in range(N):
            max_a = 0
            for dd in range(D):
                if max_a < sum(a2_list[dd][n]):
                    max_a = sum(a2_list[dd][n])
            max_a_list.append(max_a)
        # print(a2_list)
        # print(max_a_list)
        score = sum(max_a_list)
        swap_num = 0
        for n in range(N):
            for dd in range(D):
                swap_num += abs(len(a2_list[dd][n]) - 1)
        # print(score)

        if best_score >= score or math.exp((best_score - score) / (1000 - t1) * 1000) > random.random():
            print("change", best_score, score)
            best_score = score
        else:
            if ope_type == 1:
                a = a2_list[d][j].pop()
                a2_list[d][i].append(a)
            else:
                a = a2_list[d][i]
                a2_list[d][i] = a2_list[d][j]
                a2_list[d][j] = a
        if best_score <= W ** 2:
            if swap_num < best_swap:
                best_a = a2_list
            break
        # print()
print(best_a)
max_a_list = []
for n in range(N):
    max_a = 0
    for dd in range(D):
        if max_a < sum(best_a[dd][n]):
            max_a = sum(best_a[dd][n])
    max_a_list.append(max_a)
print(best_a)
print(max_a_list)
print(sum(max_a_list), max(a_sum_list))
