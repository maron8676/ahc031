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
        for i in range(N):
            rect = rects[i]
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
rect = [dict() for _ in range(D)]
for d in range(D):
    a = a_list[d]
    before = []
    if d > 0:
        before = sorted(list(rect[d - 1].values()), key=lambda x: x[0] + x[1])

    finish = False
    max_before_index = N - 1 if d > 0 else -1
    while not finish:
        rect[d] = dict()
        left = 0
        up = 0
        satisfy = True

        no_change = 0
        index_set = set(range(N))
        before_index = 0
        while before_index <= max_before_index:
            nearest = W ** 2
            nearest_index = -1
            before_rect = before[before_index]
            area = (before_rect[2] - before_rect[0]) * (before_rect[3] - before_rect[1])
            for k in index_set:
                if area >= a[k] and area - a[k] < nearest:
                    nearest = a[k]
                    nearest_index = k

            if nearest_index == -1:
                break

            if before[before_index][2] != W:
                up = before[before_index][2]
            if before[before_index][3] != W:
                left = before[before_index][3]

            index_set.remove(nearest_index)
            rect[d][nearest_index] = before[before_index]
            before_index += 1
            no_change += 1

        # print(up, left, file=sys.stderr)
        for k in range(N - no_change):
            min_rem = W
            max_index = -1
            direction = ""

            for index in index_set:
                rem_h = (W - left) - (a[index] - 1) % (W - left)
                rem_v = (W - up) - (a[index] - 1) % (W - up)

                rem = 0
                if W - up > 1 and rem_h < rem_v or W - left == 1:
                    rem = rem_h
                    if min_rem > rem:
                        min_rem = rem
                        max_index = index
                        direction = "h"
                else:
                    rem = rem_v
                    if min_rem > rem:
                        max_rem = rem
                        max_index = index
                        direction = "v"

            index_set.remove(max_index)

            # print(d, D, k, N, up, left, file=sys.stderr)
            if direction == "h":
                h = a[max_index] // (W - left)
                if a[max_index] % (W - left) != 0:
                    h += 1
                h = min(h, 2 * W - up - left - (N - k), W - up - 1)
                # print(h, W - left, a[max_index])
                if k != N - 1 - no_change:
                    rect[d][max_index] = (up, left, up + h, W)
                    if a[max_index] > h * (W - left):
                        satisfy = False
                else:
                    rect[d][max_index] = (up, left, W, W)
                    # print(a[max_index], (W - up) * (W - left), file=sys.stderr)
                    if a[max_index] > (W - up) * (W - left):
                        satisfy = False
                up += h
            else:
                v = a[max_index] // (W - up)
                if a[max_index] % (W - up) != 0:
                    v += 1
                v = min(v, 2 * W - up - left - (N - k), W - left - 1)
                # print(v, W - up, a[max_index])
                if k != N - 1 - no_change:
                    rect[d][max_index] = (up, left, W, left + v)
                    if a[max_index] > v * (W - up):
                        satisfy = False
                else:
                    rect[d][max_index] = (up, left, W, W)
                    # print(a[max_index], (W - up) * (W - left), file=sys.stderr)
                    if a[max_index] > (W - up) * (W - left):
                        satisfy = False
                left += v

        if satisfy or max_before_index == -1:
            finish = True
        else:
            max_before_index -= 1

calc_cost(D, N, a_list, rect)

# output
for d in range(D):
    for k in range(N):
        i0, j0, i1, j1 = rect[d][k]
        print(i0, j0, i1, j1)
