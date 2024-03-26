import getpass
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

# determine rectangles
rect = [[] for _ in range(D)]
for d in range(D):
    a = a_list[d]
    a_rev = a[::-1]
    left = 0
    up = 0
    for k in range(N):
        # print(d, D, k, N, up, left, file=sys.stderr)
        if (W - up) >= (W - left):
            h = a_rev[k] // (W - left)
            if a_rev[k] % (W - left) != 0:
                h += 1
            h = min(h, 2 * W - up - left - (N - k), W - up - 1)
            if k != N - 1:
                rect[d].insert(0, (up, left, up + h, W))
            else:
                rect[d].insert(0, (up, left, W, W))
            up += h
        else:
            v = a_rev[k] // (W - up)
            if a_rev[k] % (W - up) != 0:
                v += 1
            v = min(v, 2 * W - up - left - (N - k), W - left - 1)
            if k != N - 1:
                rect[d].insert(0, (up, left, W, left + v))
            else:
                rect[d].insert(0, (up, left, W, W))
            left += v

calc_cost(D, N, a_list, rect)

# output
for d in range(D):
    for k in range(N):
        i0, j0, i1, j1 = rect[d][k]
        print(i0, j0, i1, j1)
