#!/usr/bin/python3

# COMP3411 - Assignment 1 - 24T1
# Mohammad M. Rakib (z5361151)
#
# (NOTE: Please enable word wrapping in your text editor in order to be able to read these paragraphs more easily)
#
# "Briefly describe how your program works, including any algorithms and data structures employed, and explain any design decisions you made along the way:""
# 
# The following code attempts to resolve the Hashi puzzle problem using Donald Knuth's Algorithm X. Initially, I tried to use a CSP but I ran into some problems in regards to actually modelling the constraints of the entire puzzle in code. However, I found that Algorithm X, which attempts to solve the exact cover problem, allows for this modelling much more easily, since the constraints themselves can be modelled in the Algorithm X matrix.
# 
# Essentially, the exact cover problem is, given a set of subsets of a universal set, the problem of finding the right set of subsets such that every element in the universal set is contained exactly once. For example, if the universe was X = {1, 2, 3, 4}, and the subsets were A = {1, 4}, B = {1, 3, 4} and C = {2, 3}, then the exact cover would be {A, C}. Algorithm X solves this via modelling the universe and subsets in a 0-1 matrix, such as:
# X: 1  2  3  4
# A: 1  0  0  1
# B: 1  0  1  1
# C: 0  1  1  0
# and then finding the set of rows such that each column has only one 1 value in it.
# Similarly, we can model the hashi problem like this. The rows will represent all possible bridge configurations, where each bridge configuration is made out of a set of columns that consist of the 'universe' of all constraints that can define a bridge configuration.
# Then, by finding the set of rows (bridge configurations) that matches these constraints (one 1 value for each column/constraint, meaning no crossovers), we find the solution of bridge configurations.
# Here is an example for the Hashi puzzle representation.
# Consider this example:
# . . .
# 1 2 .
# . . .
# The Nodes A is (1, 0) -> 1 and Node B is (1, 1) -> 2
# Thus, the matrix will be structured as follows:
#       | Node A | Node B | Bridge 1 Start | Bridge 1 End | Bridge 1 Length | Bridge 1 Count | Bridge 2 Start | Bridge 2 End | Bridge 2 Length | Bridge 2 Count | Candidate 1 | Candidate 2 | Candidate 3 |
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Row 1 |   1    |   2    |       1        |       0      |        1        |       0        |       0        |       0      |        0        |       0        |      0      |      0      |      0      |
#Row 2 |   1    |   2    |       0        |       1      |        1        |       0        |       0        |       0      |        0        |       0        |      0      |      0      |      0      |
#Row 3 |   1    |   2    |       0        |       0      |        0        |       0        |       1        |       0      |        1        |       0        |      0      |      0      |      0      |
#Row 4 |   1    |   2    |       0        |       0      |        0        |       0        |       0        |       1      |        1        |       0        |      0      |      0      |      0      |
#

import sys

# 'product' produces a Cartesian product of iterables
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

# Reads data as an array of characters
data = sys.stdin.read().split()

# Generates all possible coordinates within the puzzle grid
coords = list(product(range(len(data)), range(len(data[0]))))

# A mapping from coordinates to lists containing possible bridges
# Each bridge is its own list of two elements: a start coordinate and an end coordinate
node_bridges = {coord: [] for coord in coords}

# A mapping from coordinates containing islands (i.e. not a dot) to the number of bridges that should be connected to that point
nodes = {(i, j): convert(data[i][j]) for i, j in coords if data[i][j] != '.'}

# A list of all possible bridges
bridges = []

# Iterates over each node, attempting to connected it to connect bridges in both horizontal and vertical directions
# If successful, bridge is added to global 'bridges' list, and to local 'node_bridges' list
for coord, count in nodes.items():

    # The (0, 1) and (1, 0) tuples represent the horizontal and vertical directions respectively
    for i, j in ((0, 1), (1, 0)):

        # Find the next coordinate in the given direction
        next_coord = coord[0] + i, coord[1] + j

        # Initialises a bridge, starting from the node coordinates, and going to 0, meaning it has no endpoint
        bridge = [coord, 0]

        # Loop while next coordinate is within bounds of coordinate grid
        while next_coord in coords:

            # Adds possible bridge locally to current node
            node_bridges[next_coord] += [bridge]

            # If the next coordinate is also a node, end point of the bridge is updated to that next coordinate
            # Then, possible bridge is added locally to current node
            # Then, possible bridge is addded globally to list of bridges
            if next_coord in nodes:
                bridge[1] = next_coord
                node_bridges[coord] += [bridge]
                bridges += [bridge]
                break

            # Find next coordinate of next coordinate in the given direction
            next_coord = next_coord[0] + i, next_coord[1] + j

# Reprocesses the node dictionary mapping to filter out any possible bridges that don't have an endpoint i.e. list representing bridge has 0 as second element
node_bridges = {x: [x for x in y if x[1] != 0] for x, y in node_bridges.items()}

# A list of possible bridge connections
candidates = [node_bridges[p] for p in coords if p not in nodes and len(node_bridges[p]) > 1]

# A matrix as used in Algorithm X
# A 2D array representing the constraints of the Hashi puzzle
# Each row corresponds to a potential configuration of bridges
# Each column corresponds to a specific aspect or constraint of the puzzle
# The # of rows depends on the total number of possible bridge configurations
# The # of columns depends on the nature of the Hashi puzzle and the specific constraints defined on the puzzle
matrix = []

# Defines the total length of each row of the matrix
# The '+ 4' represents 4 added constraints after the list of nodes, particulary: 1. start node of the bridge, 2. end node of the bridge, 3. length of bridge, 4. bridge count (0, 1, 2)
total_length = len(nodes) + 4 * len(bridges) + len(candidates)

# Keeps track of the starting index for each node in the matrix
# It is incremented to ensure that the next node's constraint information is placed in the correct position w/o overlapping with the previous node's constraint information
start = 0

# A mapping between each node to its starting index in the matrix
# Provides a convenient way to locate each node's constraint information in the matrix after it is constructed
start_nodes = {}

# Iterates over each node, generating all possible configurations of bridges connected to each node, constructing matrix rows representing these configurations
for coord, count in nodes.items():

    # Gets a list of possible bridges that can be connected to the node
    connected = node_bridges[coord]

    # Calculates the total length of bridges connected to the current node
    # It is doubled since each bridge is represented by a start and end node
    bridge_length = len(connected) * 2

    # Iterates through all possible bridge configurations between the node and each of its connected nodes
    # (0,1,2,3) is a generator expression, generating tuples containing 0, 1, 2 or 3 bridges for each connected node
    # * unpacks the generator expression to be passed as arguments to the Cartesian product function
    for t in product(*((0, 1, 2, 3) for x in connected)):

        # Calculates the sum of elements in the current bridge configuration tuple to see if it matches the expected count of the node
        # If it doesn't, skips to the next configuration
        if sum(t) != count:
            continue

        # Initialises a matrix row of 0's
        row = [0] * total_length

        # Marks the position in the matrix row where the length of the bridges connected to the current node is represented, assigning it at 1 , indicating there is a bridge of specified length connected to the current node
        row[start + bridge_length] = 1

        # Iterates over each element in the bridge configuration tupe, calculated the appropriate index in the row list based on the current configuration, selecting predefined values representing constraints based on the current configuration
        for i, x in enumerate(t):

            # Calculates index in the matrix row where the constraints related to the current bridge configuration should be placed
            # The '* 2' is due to the fact that each bridge configuration typically occupies two columns in the matrix, one for the start node and one for the end node
            k = start + i * 2

            # Accesses a tuple containing predefined values based on one of the possible configurations of a bridge x (0, 1, 2 or 3 bridges)
            # Assigns selected tuple to a slice of the row list
            row[k:k + 3] = ((1, 1, 1), (0, 1, 1), (0, 0, 1), (0, 0, 0))[x]

        # Appends row to the end of the matrix
        matrix += [row]

    # Sets the start for this node in the start_nodes dict
    start_nodes[coord] = start

    # Sets start index as 1 after the bridge length
    start += bridge_length + 1

matrix_length = len(matrix)

# Iterates over the bridges list
for bridge in bridges:

    # Bridge tuple is unpacked
    start_node, end_node = bridge

    # Initialise a matrix row
    row = [0] * total_length

    # Unpack start and end matrix indices for this particular bridge
    # start_nodes[start_node] finds the starting index of the node in the matrix row
    # node_bridges[start_node].index(bridge) finds the index of the current bridge within the list of bridges connected to the start node
    # Since each bridge occupies two columns in the matrix, we multiply index by 2
    start_index, end_index = start_nodes[start_node] + node_bridges[start_node].index(bridge) * 2, start_nodes[end_node] + node_bridges[end_node].index(bridge) * 2

    # Create a copy of the matrix row
    t = row[:]

    # Set flags for start and end index of current bridge in matrix row
    row[start_index] = row[end_index] = 1

    # Set flags for candidate bridges
    for i, u in enumerate(candidates):
        row[total_length - len(candidates) + i] = int(bridge in u)

    # Sets flags for twin row
    t[start_index + 1] = t[end_index + 1] = 1

    # We then add both matrix rows, accouting for the forward and reverse directions of bridges in the puzzle
    matrix += [row, t]

# The first four dict hold the left, right, up and down neighbours of each node respectively
# The fifth dict holds candidate solutions/configurations
left, right, up, down, candidates = {}, {}, {}, {}, {}

# Header node represents the special node that serves as the head of each column in the matrix
header = total_length

# Circularly links all the nodes, allows for efficient traversing of the matrix
left[header] = right[header] = down[header] = up[header] = header

# Efficiently traverses connected nodes until its reaches the starting node again
# Generator function yielding each connected node one by one
def get_connected_nodes(node, dir):
    connected = dir[node]
    while connected != node:
        yield connected
        connected = dir[connected]

# Adds a node to the left of the given node
def add_left(node):
    left[right[node]], right[left[node]] = left[node], right[node]
    for x in get_connected_nodes(node, down):
        for y in get_connected_nodes(x, right):
            up[down[y]], down[up[y]] = up[y], down[y]

# Adds a node to the right of the given node
def add_right(node):
    for x in get_connected_nodes(node, up):
        for y in get_connected_nodes(x, left):
            up[down[y]], down[up[y]] = y, y
    left[right[node]], right[left[node]] = node, node

# Recursively explores all poossible combinations of rows to cover the matrix
# Backtracks to undo changes and explore different paths until a solution is found
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

# Iterates over each column in the matrix, setting up necessary pointers for the doubly linked list structure
# Right pointers of the left and current columns are linked, while left pointers of the head and current columns are updated accordingly
for coord in range(total_length):
    right[left[header]], right[coord], left[header], left[coord] = coord, header, coord, left[header]
    up[coord] = down[coord] = coord

# Iterates over each row in the matrix, setting up doubly linked list structures
for index, row in enumerate(matrix):
    start_index = 0
    for col in get_connected_nodes(header, right):
        if row[col]:
            node = index, col
            down[up[col]], down[node], up[col], up[node], candidates[node] = node, col, node, up[col], col
            if start_index == 0:
                left[node] = right[node] = start_index = node
            right[left[start_index]], right[node], left[start_index], left[node] = node, start_index, node, left[start_index]

# Execute backtracking search for solution, printing each solution as it gets yielded
for solution in search():
    grid = list(map(list, data))
    for bridge in solution:
        if bridge < matrix_length:
            continue
        (i, j), (x, y) = bridges[(bridge - matrix_length) // 2]
        if j == y:
            for row in range(i + 1, x):
                if (grid[row][j] == '"'):
                    grid[row][j] = '#'
                elif (grid[row][j] == '|'):
                    grid[row][j] = '"'
                else:
                    grid[row][j] = '|'
        else:
            for col in range(j + 1, y):
                if (grid[i][col] == '='):
                    grid[i][col] = 'E'
                elif (grid[i][col] == '-'):
                    grid[i][col] = '='
                else:
                    grid[i][col] = '-'
    print('\n'.join(''.join(row) for row in grid).replace('.', ' '))
