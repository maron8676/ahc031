import bisect
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
    return cost


is_local = getpass.getuser() == "omotl"

W, D, N = li()
a_list = []
a_list_copy = [[] for _ in range(D)]
for d in range(D):
    a_list.append(li())
    a_list_copy[d].extend(a_list[d])

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

rect2 = [[] for _ in range(D)]
up = 0
left = 0
while sum([len(a) for a in a_list]) > 0:
    max_a = 0
    max_d = -1
    max_i = -1
    for d in range(D):
        if len(a_list[d]) > 0 and max_a < a_list[d][-1]:
            max_a = a_list[d][-1]
            max_d = d
            max_i = len(a_list[d]) - 1

    a = a_list[max_d]
    area = a[-1]
    rem_h = (W - left) - (area - 1) % (W - left)
    rem_v = (W - up) - (area - 1) % (W - up)

    rem = 0
    if W - up > 1 and rem_h < rem_v or W - left == 1:
        rem = rem_h
        direction = "h"
    else:
        rem = rem_v
        direction = "v"
    max_len = max([len(ai) for ai in a_list])

    size = 0
    limit = 0
    if direction == "h":
        h = area // (W - left)
        if area % (W - left) != 0:
            h += 1
        h = min(h, 2 * W - up - left - max_len - 1, W - up - 1)
        if sum([len(temp_a) for temp_a in a_list]) == 1:
            rect2[max_d].append((area, up, left, W, W))
        else:
            rect2[max_d].append((area, up, left, up + h, W))

        size = h
        limit = (W - left) * h
    else:
        v = area // (W - up)
        if area % (W - up) != 0:
            v += 1
        v = min(v, 2 * W - up - left - max_len - 1, W - left - 1)
        if sum([len(temp_a) for temp_a in a_list]) == 1:
            rect2[max_d].append((area, up, left, W, W))
        else:
            rect2[max_d].append((area, up, left, W, left + v))

        size = v
        limit = (W - up) * v

    # 他の日の分を同じ位置に詰める
    # print(max_d, limit, size, direction, up, left)
    # print("alist", a_list)
    for d in range(D):
        if d == max_d:
            continue
        ad = a_list[d]
        if len(ad) == 0:
            continue

        dp_len = min(51, len(ad) + 1)
        dp2 = [set() for _ in range(dp_len)]
        dp2[0] = {0}

        for i in range(1, dp_len):
            aa = ad[i - 1 + (len(ad) + 1 - dp_len)] // size * size
            if ad[i - 1 + (len(ad) + 1 - dp_len)] % size > 0:
                aa += size
            for dp_area in dp2[i - 1]:
                dp2[i].add(dp_area)
                dp2[i].add(dp_area + aa)

        dp2_list = list(dp2[dp_len - 1])
        dp2_list.sort()
        b_index = bisect.bisect_right(dp2_list, limit)
        b_index -= 1
        dp_sum = dp2_list[b_index]
        # print(dp_sum)

        select_a_list = []
        for i in range(dp_len - 1, 0, -1):
            aa = ad[len(ad) + 1 - dp_len + i - 1] // size * size
            if ad[len(ad) + 1 - dp_len + i - 1] % size > 0:
                aa += size
            if dp_sum - aa >= 0 and dp_sum - aa in dp2[i - 1]:
                select_a_list.append(ad[len(ad) + 1 - dp_len + i - 1])
                dp_sum -= aa
        # print(select_a_list)
        if len(select_a_list) == 0:
            rem_a = ad.pop()
            if direction == "h":
                rem_h2 = rem_a // (W - left)
                if rem_a % (W - left) != 0:
                    rem_h2 += 1
                rem_h2 = min(rem_h2, 2 * W - up - left - max_len - 1, W - up - 1)
                rect2[d].append((rem_a, up, left, up + rem_h2, W))
            else:
                rem_v2 = rem_a // (W - up)
                if rem_a % (W - up) != 0:
                    rem_v2 += 1
                rem_v2 = min(rem_v2, 2 * W - up - left - max_len - 1, W - left - 1)
                rect2[d].append((rem_a, up, left, W, left + rem_v2))

        # グループの中の最後と、全体としての最後はWまで伸ばしていい
        # if len(select_a_list) == len(ad):
        #     print(select_a_list)
        del_list = []
        if direction == "h":
            x = left
            for a_index, select_a in enumerate(select_a_list):
                index = ad.index(select_a)
                del_list.append(index)
                x_size = select_a // size
                if select_a % size > 0:
                    x_size += 1
                if a_index == len(select_a_list) - 1:
                    rect2[d].append((select_a, up, x, up + size, W))
                else:
                    rect2[d].append((select_a, up, x, up + size, x + x_size))
                x += x_size
        else:
            y = up
            for a_index, select_a in enumerate(select_a_list):
                index = ad.index(select_a)
                del_list.append(index)
                y_size = select_a // size
                if select_a % size > 0:
                    y_size += 1
                if a_index == len(select_a_list) - 1:
                    rect2[d].append((select_a, y, left, W, left + size))
                else:
                    rect2[d].append((select_a, y, left, y + y_size, left + size))
                y += y_size
        del_list.sort()
        while len(del_list) > 0:
            index = del_list.pop()
            ad.pop(index)
    if direction == "h":
        up += size
    else:
        left += size
    a.pop()
    # print()

# rect2で満たしていないものがあれば、後ろから破壊して通常方式でやり直してみる
for d in range(D):
    satisfy = True
    for rect_i in rect2[d]:
        if rect_i[0] > (rect_i[3] - rect_i[1]) * (rect_i[4] - rect_i[2]):
            satisfy = False

    # １つずつ部屋を破壊してやり直す
    # if not satisfy:
    #     print(d, rect2[d], file=sys.stderr)
    pop_num = 1
    while pop_num <= N and not satisfy:
        renewal_list = []
        for _ in range(pop_num):
            renewal_list.append(rect2[d].pop())
        # print(d, pop_num, len(rect2[d]), len(renewal_list))
        up = renewal_list[-1][1]
        left = renewal_list[-1][2]
        index_set = set(range(len(renewal_list)))

        satisfy = True
        for k in range(len(renewal_list)):
            min_rem = W
            max_index = -1
            direction = ""

            for index in index_set:
                rem_h = (W - left) - (renewal_list[index][0] - 1) % (W - left)
                rem_v = (W - up) - (renewal_list[index][0] - 1) % (W - up)

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

            # print(d, len(renewal_list), up, left, file=sys.stderr)
            if direction == "h":
                h = renewal_list[max_index][0] // (W - left)
                if renewal_list[max_index][0] % (W - left) != 0:
                    h += 1
                h = min(h, 2 * W - up - left - (len(renewal_list) - k), W - up - 1)
                # print(h, W - left, renewal_list[max_index])
                if k != len(renewal_list) - 1:
                    rect2[d].append((renewal_list[max_index][0], up, left, up + h, W))
                    if renewal_list[max_index][0] > h * (W - left):
                        satisfy = False
                else:
                    rect2[d].append((renewal_list[max_index][0], up, left, W, W))
                    # print(renewal_list[max_index], (W - up) * (W - left), file=sys.stderr)
                    if renewal_list[max_index][0] > (W - up) * (W - left):
                        satisfy = False
                up += h
            else:
                v = renewal_list[max_index][0] // (W - up)
                if renewal_list[max_index][0] % (W - up) != 0:
                    v += 1
                v = min(v, 2 * W - up - left - (len(renewal_list) - k), W - left - 1)
                # print(v, W - up, renewal_list[max_index])
                if k != len(renewal_list) - 1:
                    rect2[d].append((renewal_list[max_index][0], up, left, W, left + v))
                    if renewal_list[max_index][0] > v * (W - up):
                        satisfy = False
                else:
                    rect2[d].append((renewal_list[max_index][0], up, left, W, W))
                    # print(renewal_list[max_index], (W - up) * (W - left), file=sys.stderr)
                    if renewal_list[max_index][0] > (W - up) * (W - left):
                        satisfy = False
                left += v

        pop_num += 1

for d in range(D):
    rect2[d].sort(key=lambda x: x[0])
    for i in range(N):
        rect2[d][i] = (rect2[d][i][1], rect2[d][i][2], rect2[d][i][3], rect2[d][i][4])

# output
cost1 = calc_cost(D, N, a_list_copy, rect)
cost2 = calc_cost(D, N, a_list_copy, rect2)

# if cost1 < cost2:
#     for d in range(D):
#         for k in range(N):
#             i0, j0, i1, j1 = rect[d][k]
#             print(i0, j0, i1, j1)
# else:
for d in range(D):
    for i in range(N):
        print(*rect2[d][i])
