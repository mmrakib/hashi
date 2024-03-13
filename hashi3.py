import sys
from itertools import product as cartesian_product

input_data = sys.stdin.read().split()
length = len
enumerate_function = enumerate
range_function = range
coordinates_list = list(cartesian_product(range_function(length(input_data)), range_function(length(input_data[0]))))
connections = {(i, j): int(input_data[i][j]) for i, j in coordinates_list if '.' != input_data[i][j]}
node_items = connections.items()
bridges_list = []

adjacent_connections = {p: [] for p in coordinates_list}  # Define adjacent_connections here

for coordinate, count in node_items:
    for i, j in ((0, 1), (1, 0)):
        next_coordinate = coordinate[0] + i, coordinate[1] + j
        bridge = [coordinate, 0]
        while next_coordinate in coordinates_list:
            adjacent_connections[next_coordinate] += [bridge]
            if next_coordinate in connections:
                bridge[1] = next_coordinate
                adjacent_connections[coordinate] += [bridge]
                bridges_list += [bridge]
                break
            next_coordinate = next_coordinate[0] + i, next_coordinate[1] + j

adjacent_connections = {node: [node for node in connected_nodes if node[1] != 0] for node, connected_nodes in adjacent_connections.items()}
candidate_nodes = [adjacent_connections[coordinate] for coordinate in coordinates_list if coordinate not in connections and length(adjacent_connections[coordinate]) > 1]
bridge_matrix = []
total_length = length(connections) + 4 * length(bridges_list) + length(candidate_nodes)
start_index = 0
node_start_indices = {}

for coordinate, count in node_items:
    connected_nodes = adjacent_connections[coordinate]
    bridge_length = length(connected_nodes) * 2
    for combinations in cartesian_product(*((0, 1, 2) for _ in connected_nodes)):
        if sum(combinations) != count:
            continue
        bridge_row = [0] * total_length
        bridge_row[start_index + bridge_length] = 1
        for index, connection_type in enumerate_function(combinations):
            bridge_index = start_index + index * 2
            bridge_row[bridge_index:bridge_index + 2] = ((1, 1), (0, 1), (0, 0))[connection_type]
        bridge_matrix += [bridge_row]
    node_start_indices[coordinate] = start_index
    start_index += bridge_length + 1

bridge_matrix_length = length(bridge_matrix)

for bridge in bridges_list:
    start_node, end_node = bridge
    bridge_row = [0] * total_length
    start_index = node_start_indices[start_node]
    end_index = node_start_indices[end_node]
    temporary_row = bridge_row[:]
    bridge_row[start_index] = bridge_row[end_index] = 1
    for index, connected_nodes in enumerate_function(candidate_nodes):
        bridge_row[total_length - length(candidate_nodes) + index] = int(bridge in connected_nodes)
    temporary_row[start_index + 1] = temporary_row[end_index + 1] = 1
    bridge_matrix += [bridge_row, temporary_row]

def get_connected_nodes(node, direction):
    connected_node = direction[node]
    while connected_node != node:
        yield connected_node
        connected_node = direction[connected_node]

def add_to_left(node):
    right_of_left[node], left_of_right[node] = left_of_right[node], right_of_left[node]
    for connected_node in get_connected_nodes(node, down_of):
        for adjacent_node in get_connected_nodes(connected_node, right_of_left):
            up_of[down_of[adjacent_node]], down_of[up_of[adjacent_node]] = up_of[adjacent_node], down_of[up_of[adjacent_node]]

def add_to_right(node):
    for connected_node in get_connected_nodes(node, up_of):
        for adjacent_node in get_connected_nodes(connected_node, left_of_right):
            right_of_left[down_of[adjacent_node]], left_of_right[up_of[adjacent_node]] = left_of_right[up_of[adjacent_node]], down_of[adjacent_node]
    right_of_left[node], left_of_right[node] = node, node

def find_solution():
    current_node = right_of_left[last_node]
    if current_node == last_node:
        yield []
    add_to_left(current_node)
    for bridge_node in get_connected_nodes(current_node, down_of):
        for adjacent_node in get_connected_nodes(bridge_node, right_of_left):
            add_to_right(candidate_nodes[adjacent_node])
        for solution in find_solution():
            yield [bridge_node[0]] + solution
        for adjacent_node in get_connected_nodes(bridge_node, left_of_right):
            add_to_left(candidate_nodes[adjacent_node])
    add_to_right(current_node)

right_of_left, left_of_right, up_of, down_of, candidate_nodes = {}, {}, {}, {}, {}
last_node = total_length
right_of_left[last_node] = left_of_right[last_node] = down_of[last_node] = up_of[last_node] = last_node

for node_index in range_function(total_length):
    right_of_left[last_node], right_of_left[node_index], left_of_right[last_node], left_of_right[node_index] = node_index, last_node, node_index, right_of_left[last_node]
    up_of[node_index] = down_of[node_index] = candidate_nodes[node_index] = node_index

for index, bridge_row in enumerate_function(bridge_matrix):
    start_index = 0
    for node_index in get_connected_nodes(last_node, right_of_left):
        if bridge_row[node_index]:
            node = index, node_index
            down_of[up_of[node_index]], down_of[node], up_of[node_index], up_of[node], candidate_nodes[node] = node, node_index, node, up_of[node_index], node_index
            if start_index == 0:
                right_of_left[node], left_of_right[node] = start_index = node, node
            right_of_left[left_of_right[start_index]], right_of_left[node], left_of_right[node], left_of_right[start_index] = node, start_index, node, left_of_right[start_index]
    for node_index in get_connected_nodes(last_node, right_of_left):
        start_index, right_of_left[start_index], right_of_left[node_index], left_of_right[start_index], left_of_right[node_index] = node_index, node_index, last_node, node_index, node_index

for solution in find_solution():
    puzzle_grid = list(map(list, input_data))
    for bridge_node in solution:
        if bridge_node < bridge_matrix_length:
            continue
        (i, j), (x, y) = bridges_list[(bridge_node - bridge_matrix_length) // 2]
        if j == y:
            for row_index in range_function(i + 1, x):
                puzzle_grid[row_index][j] = '|H'[puzzle_grid[row_index][j] == '|']
        else:
            for column_index in range_function(j + 1, y):
                puzzle_grid[i][column_index] = '-='[puzzle_grid[i][column_index] == '-']
    print('\n'.join(''.join(row) for row in puzzle_grid).replace('.', ' '))
