#!/usr/bin/python3

# Import required libraries, including system functions and the cartesian product
import sys
from itertools import product

# Read input data and prcoess it
data = sys.stdin.read().split() # Reads input data from stdin as an array of characters
coords = list(product(range(len(data)), range(len(data[0])))) # Generates map of all possible coordinates in the grid
points = {coord: [] for coord in coords} # Creates a mapping from each coordinate to a list containing metadata, empty for now
nodes = {(i, j): int(data[i][j]) for i, j in coords if data[i][j] != '.'} # Generates a mapping from each coordinate to its contained value if and only if it is an island, not if its empty (i.e. a dot)
bridges = [] # An empty list of bridges

# Detect possible bridges and add them as possible bridges both globally and locally per point in points dictionary containing metadata
for coord, count in nodes.items(): # .items() returns a list of (key, value) tuples from the dict, with each tuple containing the coordinate and its contained value 'count'
    for i, j in ((0, 1), (1, 0)): # (0, 1) and (1, 0) represent right and down directions respectively; this loop thus moves the grid down from the top left
        next_coord = coord[0] + i, coord[1] + j # Gets the next coordinate in the specified direction
        bridge = [coord, 0] # A list representing a bridge, with a coordinate and a value of 0 stating no other point is connected to the coordinate
        while next_coord in coords: # Explores adjacent coordinates
            points[next_coord] += [bridge] # Appends the current bridge to the list of bridges associated with the next coordinate
            if next_coord in nodes: # If the next coordinate is a coordinate containing a node
                bridge[1] = next_coord # Sets bridge end point of initial 0 value to the next coordinate to represent a possible bridge
                points[coord] += [bridge] # Add to local list of bridges for the given point
                bridges += [bridge] # Add to global list of bridges
                break # Break out of loop since we've either found a node or reached the end of the coordinate map, meaning we don't need to look any further for an endpoint
            next_coord = next_coord[0] + i, next_coord[1] + j # If no possible bridge found, move to the next coordinate

# Reprocess input based off of detected bridges
points = {x: [x for x in y if x[1] != 0] for x, y in points.items()} # Reconstructs the points dict by filtering out any bridges in the metadata where the endpoints do not connected (i.e. are 0)
candidates = [points[p] for p in coords if p not in nodes and len(points[p]) > 1] # Selects coordinates that are not nodes and have more than one possible bridge connected them, essentially points where bridges can be built

# Set up matrix representation of the puzzle
matrix = [] # Contains binary representation of puzzle constraints and bridge connections
total_length = len(nodes) + 4 * len(bridges) + len(candidates) # Total number of columns needed to represent puzzle constraints and bridge connections; since each bridge can be represented by two binary values (start and end point), and each potential bridge can have up to two bridges, we multiply the number of nodes by 4
start = 0 # Used to the track the column number for constraints in each row of the matrix
start_nodes = {} # Stores the starting index of bridge constraints for each node in the puzzle, such that the key is a coordinate tuple, and the value is the corresponding starting index in the matrix for the bridge constraints associated with that node

# Populate matrix representation of the puzzle
for coord, count in nodes.items(): # .items() returns a list of (key, value) tuples from the dict, with each tuple containing the coordinate and its contained value 'count'
    connected = points[coord] # Gets list of bridges connected to the current point
    bridge_length = len(connected) * 2 # Represents total length of bridge constraints associated with the current node, each bridge constraint occupying two columns in the matrix: start point and end point
    for t in product(*((0, 1, 2) for x in connected)): # Generates all possible combinations of bridge configurations for the bridges connected to the current node, with the tuple (0, 1, 2) representing possible bridge values
        if sum(t) != count: # Checks if the sum of the configurations in t matches the required count for the code, if not, that means current configuration does not satisfy the node constraints and thus the loop continues
            continue
        row = [0] * total_length # An empty list representing a row in the constraints matrix
        row[start + bridge_length] = 1 # start is starting index of bridge constraints, bridge_length is total lenght of bridge constraints; this line marks the position in the row where the bridge constraints for the current node starts
        for i, x in enumerate(t): # Iterates over the possible combinations of bridge configurations
            k = start + i * 2 # Calculates the index in the constraints matrix row where the bridge constraint for the current bridge configuration starts, with each bridge constraint occupying two columns in the matrix, which is why its i * 2
            row[k:k + 2] = ((1, 1), (0, 1), (0, 0))[x] # Assigns the appropriate bridge constraint in the corresponding positions in the row based on the current bridge configuration x; ((1,1), (0,1), (0,0)) represents the possible bridge configurations: (0,0) no bridge, (0, 1) 1 bridge, (1,1) 2 bridges
        matrix += [row] # Appends row, containing bridge constraints for the current node, to the constraints matrix, with each row representing one possible configuration of bridges connected to the current node
    start_nodes[coord] = start # Stores starting index of bridge constraints for the current node in the start_nodes dict
    start += bridge_length + 1 # Updates the value of start to prepare for the next node's bridge constraints, bridge_length is the total length of bridge constraints and 1 separates this set to the next node's set of bridge constraints

matrix_length = len(matrix) # Number of rows in the matrix

for bridge in bridges: # Iterates for each bridge in the list of possible bridges
    start_node, end_node = bridge # Unpacks each bridge into starting and ending nodes
    row = [0] * total_length # An empty constraints matrix row
    start_index, end_index = start_nodes[start_node] + points[start_node].index(bridge) * 2, start_nodes[end_node] + points[end_node].index(bridge) * 2 # Calculates the indices in the row list where the bridge constraints for the current bridge start and end, using the start_nodes dict; the multiplication by 2 represents the fact that each bridge constraint occupies two columns in the matrix
    t = row[:] # Creates a copy of the constraints matrix row
    row[start_index] = row[end_index] = 1 # Marks positions in the bridge matrix where the bridge constraints for the current bridge start and end
    for i, u in enumerate(candidates): # i is index of current candidate point, u is list of bridges connected to that candidate
        row[total_length - len(candidates) + i] = int(bridge in u) # Sets value in the row corresponding to current candidate, checks if current bridge is connected to current candidate
    t[start_index + 1] = t[end_index + 1] = 1 # Marks position in the t row where bridge constraints for current bridge start and end
    matrix += [row, t] # Adds bridge constraint to matrix, with each bridge constraint represented by two rows in the matrix for both start and end of the bridge

# Prepare data structures required for search algorithm
left, right, up, down, candidates = {}, {}, {}, {}, {} # These five dictionaries represent the connections between node and bridge constraints in the constraints matrix
header = total_length # Represents top of the matrix
left[header] = right[header] = down[header] = up[header] = header # Creates circular references so dead ends are never reached

# Implement search algorithm
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

# Populate data structures required to perform search
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

# Execute search and print out solution
for solution in search(): # Iterates over each solution generated by the solution() generator function
    grid = list(map(list, data)) # Represents the grid of the puzzle as a 2D array of characters
    for bridge in solution: # Iterates over each bridge in the curren solution
        if bridge < matrix_length: # Bridges with indices less than matrix length are connections between nodes, and are thus skipped
            continue
        (i, j), (x, y) = bridges[(bridge - matrix_length) // 2] # Retrieves the coordinates of the bridge from the bridge list
        if j == y: # Checks if the bridge is oriented horizontally
            for row in range(i + 1, x):
                # Check if the character at grid[row][j] is '|'
                if grid[row][j] == '|':
                    # If it is, assign 'H' to grid[row][j]
                    grid[row][j] = 'H'
                else:
                    # If it's not, assign '|' to grid[row][j]
                    grid[row][j] = '|'
        else:
            for col in range(j + 1, y):
                # Check if the character at grid[i][col] is '-'
                if grid[i][col] == '-':
                    # If it is, assign '=' to grid[i][col]
                    grid[i][col] = '='
                else:
                    # If it's not, leave it unchanged
                    grid[i][col] = '-'

    print('\n'.join(''.join(row) for row in grid).replace('.', ' '))
