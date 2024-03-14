#!/usr/bin/python3

import sys
from itertools import product

data = sys.stdin.read().split()
coords = list(product(range(len(data)), range(len(data[0]))))
points = {coord: [] for coord in coords}
nodes = {(i, j): int(data[i][j]) for i, j in coords if data[i][j] != '.'}
bridges = []

for coord, count in nodes.items():
    for i, j in ((0, 1), (1, 0)):
        next_coord = coord[0] + i, coord[1] + j
        bridge = [coord, 0]
        while next_coord in coords:
            points[next_coord] += [bridge]
            if next_coord in nodes:
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
start_nodes = {}

for coord, count in nodes.items():
    connected = points[coord]
    bridge_length = len(connected) * 2
    for t in product(*((0, 1, 2) for x in connected)):
        if sum(t) != count:
            continue
        row = [0] * total_length
        row[start + bridge_length] = 1
        for i, x in enumerate(t):
            k = start + i * 2
            row[k:k + 2] = ((1, 1), (0, 1), (0, 0))[x]
        matrix += [row]
    start_nodes[coord] = start
    start += bridge_length + 1

matrix_length = len(matrix)

for bridge in bridges:
    start_node, end_node = bridge
    row = [0] * total_length
    start_index, end_index = start_nodes[start_node] + points[start_node].index(bridge) * 2, start_nodes[end_node] + points[end_node].index(bridge) * 2
    t = row[:]
    row[start_index] = row[end_index] = 1
    for i, u in enumerate(candidates):
        row[total_length - len(candidates) + i] = int(bridge in u)
    t[start_index + 1] = t[end_index + 1] = 1
    matrix += [row, t]

left, right, up, down, candidates = {}, {}, {}, {}, {}
header = total_length
left[header] = right[header] = down[header] = up[header] = header

def get_connected_nodes(node, dir):
    connected = dir[node]
    while connected != node:
        yield connected
        connected = dir[connected]

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
    node = right[header]
    if node == header:
        yield []
    add_left(node)
    for row in get_connected_nodes(node, down):
        for connected in get_connected_nodes(row, right):
            add_left(candidates[connected])
        for t in search():
            yield [row[0]] + t
        for connected in get_connected_nodes(row, left):
            add_right(candidates[connected])
    add_right(node)

for coord in range(total_length):
    right[left[header]], right[coord], left[header], left[coord] = coord, header, coord, left[header]
    up[coord] = down[coord] = coord

for index, row in enumerate(matrix):
    start_index = 0
    for col in get_connected_nodes(header, right):
        if row[col]:
            node = index, col
            down[up[col]], down[node], up[col], up[node], candidates[node] = node, col, node, up[col], col
            if start_index == 0:
                left[node] = right[node] = start_index = node
            right[left[start_index]], right[node], left[start_index], left[node] = node, start_index, node, left[start_index]

for solution in search():
    grid = list(map(list, data))
    for bridge in solution:
        if bridge < matrix_length:
            continue
        (i, j), (x, y) = bridges[(bridge - matrix_length) // 2]
        if j == y:
            for row in range(i + 1, x):
                # grid[row][j] = '|H'[grid[row][j] == '|']
                if (grid[row][j] == '"'):
                    grid[row][j] = '#'
                elif (grid[row][j] == '|'):
                    grid[row][j] = '"'
                else:
                    grid[row][j] = '|'
        else:
            for col in range(j + 1, y):
                # grid[i][col] = '-='[grid[i][col] == '-']
                if (grid[i][col] == '='):
                    grid[i][col] = 'E'
                elif (grid[i][col] == '-'):
                    grid[i][col] = '='
                else:
                    grid[i][col] = '-'
    print('\n'.join(''.join(row) for row in grid).replace('.', ' '))
