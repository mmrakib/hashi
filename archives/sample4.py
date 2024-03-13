import sys
from itertools import product as cartesian_product

# Read input from standard input
input_lines = sys.stdin.read().split()

# Define helper functions
to_list = list
length = len
enumerate_indices = enumerate
iterate_range = range

# Generate all possible coordinates for the puzzle grid
grid_coordinates = to_list(cartesian_product(iterate_range(length(input_lines)), iterate_range(length(input_lines[0]))))

# Initialize a dictionary to represent connections between grid points
connections = {coordinate: [] for coordinate in grid_coordinates}

# Extract the islands and their numbers into a dictionary
islands = {(i, j): int(input_lines[i][j]) for i, j in grid_coordinates if input_lines[i][j] != '.'}

# Initialize a list to store bridges
bridges = []

# Build the graph by populating connections between adjacent islands
for point, count in islands.items():
    for increment_i, increment_j in ((0, 1), (1, 0)):
        current_point = point[0] + increment_i, point[1] + increment_j
        edge = [point, 0]  # Represents a bridge between two points, initially with no connection
        while current_point in grid_coordinates:
            connections[current_point].append(edge)
            if current_point in islands:
                edge[1] = current_point  # Mark the endpoint of the bridge if it reaches an island
                connections[point].append(edge)
                bridges.append(edge)
                break
            current_point = current_point[0] + increment_i, current_point[1] + increment_j

# Remove unnecessary bridges and handle constraints
connections = {point: [connection for connection in connections_list if connection[1] != 0] for point, connections_list in connections.items()}
candidates = [connections[point] for point in grid_coordinates if point not in islands and length(connections[point]) > 1]

# Create a matrix to represent constraints for the bridge connections
constraints_matrix = []

# Calculate the size of the constraints matrix
constraints_size = length(islands) + 4 * length(bridges) + length(candidates)

# Initialize indexes and pointers for Dancing Links algorithm
left, right, up, down, column_header = {}, {}, {}, {}, {}

# Initialize the root node
header = constraints_size
left[header] = right[header] = down[header] = up[header] = header

# Initialize doubly linked lists for the Dancing Links algorithm
for constraint_index, constraint_list in enumerate(bridges):
    constraint_size = length(constraint_list) * 2
    column_header[constraint_index] = constraints_size + constraint_index
    current_header = column_header[constraint_index]
    left[current_header] = right[current_header] = up[current_header] = down[current_header] = current_header
    left[current_header + 1] = right[current_header + 1] = up[current_header + 1] = down[current_header + 1] = current_header + 1
    left[right[header]], right[current_header], left[current_header], right[header] = current_header, current_header + 1, right[header], current_header
    up[current_header + 1] = down[current_header + 1] = up[header]
    down[up[header]] = down[current_header + 1] = current_header + 1
    for constraint in constraint_list:
        if constraint[1]:
            row_index, column_index = constraint[0], constraint[1]
            new_node = row_index, column_index
            down[up[new_node]], down[new_node], up[new_node], up[down[new_node]] = new_node, new_node, up[new_node], new_node
            down[new_node], down[up[current_header + 1]] = up[current_header + 1], new_node
            up[new_node], up[current_header + 1] = current_header + 1, new_node

# Solve the puzzle using Dancing Links algorithm
def remove_node(column):
    right[left[column]], left[right[column]] = right[column], left[column]
    for row in iterate_nodes(column, down):
        for neighbor in iterate_nodes(row, right):
            up[down[neighbor]], down[up[neighbor]] = up[neighbor], down[neighbor]

def restore_node(column):
    for row in iterate_nodes(column, up):
        for neighbor in iterate_nodes(row, left):
            up[down[neighbor]], down[up[neighbor]] = neighbor, neighbor
    right[left[column]], left[right[column]] = column, column

def iterate_nodes(start_node, direction):
    current_node = direction[start_node]
    while current_node != start_node:
        yield current_node
        current_node = direction[current_node]

def search_solutions():
    column = right[header]
    if column == header:
        yield []
    else:
        remove_node(column)
        for row in iterate_nodes(column, down):
            for neighbor in iterate_nodes(row, right):
                remove_node(column_header[neighbor])
            for solution in search_solutions():
                yield [row[0]] + solution
            for neighbor in iterate_nodes(row, left):
                restore_node(column_header[neighbor])
        restore_node(column)

# Find and print solutions
for solution in search_solutions():
    board = to_list(to_list(row) for row in input_lines)
    for bridge_index in solution:
        if bridge_index < length(islands):
            continue
        bridge = bridges[(bridge_index - length(islands)) // 2]
        (i, j), (x, y) = bridge
        if j == y:
            for row in iterate_range(i + 1, x):
                board[row][j] = '|H'[board[row][j] == '|']
        else:
            for col in iterate_range(j + 1, y):
                board[i][col] = '-='[board[i][col] == '-']
    print('\n'.join(''.join(row) for row in board).replace('.', ' '))
