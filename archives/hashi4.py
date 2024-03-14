#!/usr/bin/python3

import sys
from itertools import product

def convert(ch):
    if (ch.isdigit()):
        return int(ch)
    elif (ch == 'a'):
        return 10
    elif (ch == 'b'):
        return 11
    elif (ch == 'c'):
        return 12

data = sys.stdin.read().split()
coords = list(product(range(len(data)), range(len(data[0]))))
points = {coord: [] for coord in coords}
nodes = {(i, j): convert(data[i][j]) for i, j in coords if data[i][j] != '.'}
bridges = []

for coord, count in nodes.items():
    for i, j in ((0, 1), (1, 0)):
        next_coord = coord[0] + i, coord[1] + j
        bridge = [coord, 0]
        while next_coord in coords:
            points[next_coord] += [bridge]
            if next_coord in nodes.items():
                bridge[1] = next_coord
                points[coord] += [bridge]
                bridges += [bridge]
                break
            next_coord = next_coord[0] + i, next_coord[1] + j

points = {x: [x for x in y if x[1] != 0] for x, y in points.items()}
candidates = [points[p] for p in coords if p not in nodes and len(points[p]) > 1]
matrix = []
total_length = len(nodes) + 4 * len(bridges) + len(candidates)
start = 0
l = {}

for coord, count in nodes.items():
    e = points[coord]
    u = len(e) * 2
    for t in product(*((0, 1, 2) for x in e)):
        if sum(t) != count:
            continue
        row = [0] * total_length
        row[start + u] = 1
        for i, x in enumerate(t):
            k = start + i * 2
            row[k:k + 2] = ((1, 1), (0, 1), (0, 0))[x]
        matrix += [row]
    l[coord] = start
    start += u + 1

matrix_length = len(matrix)
for bridge in bridges:
    start_node, end_node = bridge
    row = [0] * total_length
    start_index, end_index = l[start_node] + points[start_node].index(e) * 2, l[end_node] + points[end_node].index(e) * 2
    t = row[:]
    row[start_index] = row[end_index] = 1
    for i, u in enumerate(candidates):
        row[total_length - len(candidates) + i] = int(e in u)
    t[start_index + 1] = t[end_index + 1] = 1
    matrix += [row, t]

def get_connected_nodes(node, direction):
    connected_node = direction[node]
    while connected_node != node:
        yield connected_node
        connected_node = direction[connected_node]

def add_left(node):
    left[right[node]], right[left[node]] = left[node], right[node]
    for x in get_connected_nodes(node, down):
        for y in get_connected_nodes(x, right):
            up[down[y]], down[up[y]] = up[y], down[y]

def add_right(node):
    for x in get_connected_nodes(node, up):
        for y in get_connected_nodes(x, left):
            up[down[y]], down[up[y]] = y, y
    left[right[node]], right[left[node]] = node, node

def search():
    node = right[last]
    if node == last:
        yield []
    add_left(node)
    for row in get_connected_nodes(node, down):
        for x in get_connected_nodes(row, right):
            add_left(C[x])
        for t in search():
            yield [row[0]] + t
        for x in get_connected_nodes(row, left):
            add_right(C[x])
    add_right(node)

left, right, up, down, C = {}, {}, {}, {}, {}
last = total_length
left[last] = right[last] = down[last] = up[last] = last

for coord in range(total_length):
    right[left[last]], right[coord], left[last], left[coord] = coord, last, coord, left[last]
    up[coord] = down[coord] = coord

for i, l in enumerate(matrix):
    s = 0
    for node in get_connected_nodes(last, right):
        if l[node]:
            r = i, node
            down[up[node]], down[r], up[node], up[r], C[r] = r, node, r, up[node], node
            if s == 0:
                left[r] = right[r] = s = r
            right[left[s]], right[r], left[s], left[r] = r, s, r, left[s]

for s in search():
    b = list(map(list, data))
    for e in s:
        if e < matrix_length:
            continue
        (i, j), (x, y) = bridges[(e - matrix_length) // 2]
        if j == y:
            for r in range(i + 1, x):
                b[r][j] = '|H'[b[r][j] == '|']
        else:
            for r in range(j + 1, y):
                b[i][r] = '-='[b[i][r] == '-']
    print('\n'.join(''.join(l) for l in b).replace('.', ' '))
