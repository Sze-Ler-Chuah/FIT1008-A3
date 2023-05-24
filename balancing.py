from __future__ import annotations
from threedeebeetree import Point
from ratio import Percentiles

def make_ordering(my_coordinate_list: list[Point]) -> list[Point]:
    result = []
    balancing(my_coordinate_list, result)
    return result

def balancing(my_coordinate_list: list[Point], result: list[Point]):
    x1, y1, z1 = percentile_xyz(my_coordinate_list)
    if len(my_coordinate_list) < 18:
        result.extend(my_coordinate_list)
        return
    x, y, z = x1.ratio(12.5, 12.5), y1.ratio(12.5, 12.5), z1.ratio(12.5, 12.5)
    point = search_points(x, y, z, len(x) // 2, -1, -1)
    result.append(point)
    for child in space(my_coordinate_list, point):
        balancing(child, result)


def search_points(x_list: list[Point], y_bound: list[Point], z_bound: list[Point], start: int, end: int, step: int) -> Point:
    for index in range(len(x_list)):
        #if x_list[index][1] >= y_bound[0] and x_list[index][1] <= y_bound[-1] and x_list[index][2] >= z_bound[0] and x_list[index][2] <= z_bound[-1]:
        if x_list[index][1] in y_bound and x_list[index][2] in z_bound:
            return x_list[index]
def space(my_coordinate_list: list[Point], point: Point):
    child = [[], [], [], [], [], [], [], []]
    for i in my_coordinate_list:
        if i == point:
            continue
        index = calc_index(i, point)
        child[index].append(i)
    return child

def percentile_xyz(my_coordinate_list: list[Point]):
    x, y, z = Percentiles(), Percentiles(), Percentiles()
    for i in my_coordinate_list:
        x.add_point(i)
        y.add_point(i[1])
        z.add_point(i[2])
    return x, y, z

def calc_index(current: Point, other: Point) -> int:
    sum = 0
    if current[0] >= other[0]:
        sum += 4
    if current[1] >= other[1]:
        sum += 2
    if current[2] >= other[2]:
        sum += 1
    return sum


if __name__ == "__main__":
    from threedeebeetree import Point, ThreeDeeBeeTree
    import random


    def get_size(node):
        if node is None:
            return 0
        return node.subtree_size


    # Testing function to calculate the worst ratio on your 3️⃣🇩🐝🌳
    def collect_worst_ratio(node):
        default = (1, 0, "")
        if node is None:
            return default
        root_level = node.key
        neg_x_pos_y_pos_z = node.get_child_for_key((root_level[0] - 1, root_level[1] + 1, root_level[2] + 1))
        neg_x_pos_y_neg_z = node.get_child_for_key((root_level[0] - 1, root_level[1] + 1, root_level[2] - 1))
        neg_x_neg_y_pos_z = node.get_child_for_key((root_level[0] - 1, root_level[1] - 1, root_level[2] + 1))
        neg_x_neg_y_neg_z = node.get_child_for_key((root_level[0] - 1, root_level[1] - 1, root_level[2] - 1))
        pos_x_pos_y_pos_z = node.get_child_for_key((root_level[0] + 1, root_level[1] + 1, root_level[2] + 1))
        pos_x_pos_y_neg_z = node.get_child_for_key((root_level[0] + 1, root_level[1] + 1, root_level[2] - 1))
        pos_x_neg_y_pos_z = node.get_child_for_key((root_level[0] + 1, root_level[1] - 1, root_level[2] + 1))
        pos_x_neg_y_neg_z = node.get_child_for_key((root_level[0] + 1, root_level[1] - 1, root_level[2] - 1))
        pos_x = sum(get_size(n) for n in [
            pos_x_neg_y_neg_z,
            pos_x_neg_y_pos_z,
            pos_x_pos_y_neg_z,
            pos_x_pos_y_pos_z,
        ])
        neg_x = sum(get_size(n) for n in [
            neg_x_neg_y_neg_z,
            neg_x_neg_y_pos_z,
            neg_x_pos_y_neg_z,
            neg_x_pos_y_pos_z,
        ])
        pos_y = sum(get_size(n) for n in [
            neg_x_pos_y_neg_z,
            neg_x_pos_y_pos_z,
            pos_x_pos_y_neg_z,
            pos_x_pos_y_pos_z,
        ])
        neg_y = sum(get_size(n) for n in [
            neg_x_neg_y_neg_z,
            neg_x_neg_y_pos_z,
            pos_x_neg_y_neg_z,
            pos_x_neg_y_pos_z,
        ])
        pos_z = sum(get_size(n) for n in [
            neg_x_neg_y_pos_z,
            neg_x_pos_y_pos_z,
            pos_x_neg_y_pos_z,
            pos_x_pos_y_pos_z,
        ])
        neg_z = sum(get_size(n) for n in [
            neg_x_neg_y_neg_z,
            neg_x_pos_y_neg_z,
            pos_x_neg_y_neg_z,
            pos_x_pos_y_neg_z,
        ])
        if pos_x >= 19 or neg_x >= 19:
            try:
                default = max(default, (pos_x / neg_x, neg_x, "x"), (neg_x / pos_x, pos_x, "x"))
            except ZeroDivisionError:
                default = (float('inf'), (pos_x, neg_x), "x")
        if pos_y >= 19 or neg_y >= 19:
            try:
                default = max(default, (pos_y / neg_y, neg_y, "y"), (neg_y / pos_y, pos_y, "y"))
            except ZeroDivisionError:
                default = (float('inf'), (pos_y, neg_y), "y")
        if pos_z >= 19 or neg_z >= 19:
            try:
                default = max(default, (pos_z / neg_z, neg_z, "z"), (neg_z / pos_z, pos_z, "z"))
            except ZeroDivisionError:
                default = (float('inf'), (pos_z, neg_z), "z")
        return max(default, default, *(collect_worst_ratio(child) for child in [
            neg_x_neg_y_neg_z,
            neg_x_neg_y_pos_z,
            neg_x_pos_y_neg_z,
            neg_x_pos_y_pos_z,
            pos_x_neg_y_neg_z,
            pos_x_neg_y_pos_z,
            pos_x_pos_y_neg_z,
            pos_x_pos_y_pos_z,
        ]))


    for j in range(1000):
        last = j + 1
        points = []
        coords = list(range(10000))
        random.shuffle(coords)
        for i in range(3000):
            point = (coords[3 * i], coords[3 * i + 1], coords[3 * i + 2])
            points.append(point)

        # for i in points:
        #     print(i)
        ordering = make_ordering(points)
        # for i in ordering:
        #     print(i)
        tdbt = ThreeDeeBeeTree()
        for i, p in enumerate(ordering):
            tdbt[p] = i

        ratio, smaller, axis = collect_worst_ratio(tdbt.root)

        # print(j)
        assert len(ordering), 3000
        assert ratio <= 7, True
        # print(ordering[0:10])
        print(ratio)
    print(last)

