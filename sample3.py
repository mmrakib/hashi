# Module for system related functions/parameters
import sys

# Module for iterator related functions/parameters, 
# 'product' returns cartesidan product
# 'combinations' returns r-length subsets of a set
from itertools import product, combinations # 

# Possible bridge configurations
bridges = []

# Puzzle grid, read from input file specified as command line argument
# Each grid cell is either a tuple of (row, col, value, []) if island or 0 if water
grid = [[[0, (row, col, cell, [])][cell != '.'] for col, cell in enumerate(line.strip())] for row, line in enumerate(open(sys.argv[1]))]

# Number of rows and columns of grid respectively
rows = range(len(grid))
cols = range(len(grid[0]))

# Find possible bridge configurations
# Iterates over all possible pairs of points in grid, checking if both are valid islands and form a valid bridge configuration
# Valid bridge configurations are added to the bridges list as a tuple (point1, point2, row_indices, col_indices, is_horizontal)
# 'point1' and 'point2' contain coordinates of the two points that have a valid bridge configuration
# If the bridge is horizontal, 'row_indices' contains a single value containing the row index for the bridge and 'col_indices' contains values of the cells bridge covers
# If the bridge is vertical, 'col_indices' contains a single value containing the col index for the bridge and 'row_indices' contains values of the cells bridge covers
# 'is_horizontal' defines orientation of bridge
for point1, point2 in combinations(product(rows, cols), 2):
    row1, col1 = point1
    row2, col2 = point2
    
    if grid[row1][col1] and grid[row2][col2]:
        if row1 == row2 and abs(col1 - col2) > 1:
            is_horizontal = True
            gap_range = range(min(col1, col2) + 1, max(col1, col2))
            is_valid = all(grid[row1][col] == 0 for col in gap_range)
            if is_valid:
                bridges.append((point1, point2, [row1], gap_range, is_horizontal))
        
        if col1 == col2 and abs(row1 - row2) > 1:
            is_horizontal = False
            gap_range = range(min(row1, row2) + 1, max(row1, row2))
            is_valid = all(grid[row][col1] == 0 for row in gap_range)
            if is_valid:
                bridges.append((point1, point2, gap_range, [col1], is_horizontal))

# A recursive function that tries to solve puzzle using backtracking, recursively trying different possible bridge configurations until they lead to a valid solution
# 'values' is a parameter representing the current configuration of bridges
# 'index' is a parameter representing the index of the current bridge configuration being considered
# 'mapping' is a dictionary parameter representing the mapping of island points to the total number of bridges connected to them
def solve_bridge_configurations(values, index, mapping):
    # Base case
    # If index exceeds length of 'values' list, means all bridges have been assigned, thus function returns None to indicate failure
    if index >= len(values):
        return None
    
    # Iterates over possible values for current bridge configuration
    for j in [2, 1, 0]:
        # Updates value list with current configuration value
        values[index] = j

        # Copies mapping dictionary to ensure each recursive call operates on a clean slate
        temp_mapping = dict(mapping)

        # Checks if current bridge configuration is valid
        is_valid = True
        for l in [0, 1]: # Indices for two island points in a bridge
            # Gets currently indexed possible bridge and corresponding island point (one of the two)
            point = bridges[index][l]

            # If point is not already in the mapping dictionary, adds it with zero bridges connected
            if point not in temp_mapping:
                temp_mapping[point] = 0

            # Adds current configuration value to mapped point value
            temp_mapping[point] += j

            # Gets island value from grid
            island_value = int(grid[point[0]][point[1]][0])

            # If the number of bridges connected is more than the current value, the configuration is invalid
            if temp_mapping[point] > island_value:
                is_valid = False
        
        # If not valid, go to next value for bridge configuration
        if not is_valid:
            continue
        
        # Checks for overlapping bridges
        bridge_pairs = [(direction1, direction2) for bridge_index in range(index + 1) for direction1, direction2 in product(bridges[bridge_index][2], bridges[bridge_index][3]) if values[bridge_index] > 0]
        if len(bridge_pairs) != len(set(bridge_pairs)):
            continue
        
        # Checks completeness of solution
        if index == len(values) - 1:
            is_complete = True
            for row, col in product(rows, cols):
                island = grid[row][col]
                if not island:
                    continue
                if temp_mapping[(island[1], island[2])] != int(island[0]):
                    is_complete = False
                    break
            if is_complete:
                return values
        
        # Recursively explores bridge configurations
        result = solve_bridge_configurations(values, index + 1, temp_mapping)
        if result:
            return result

# Solve the puzzle
values = solve_bridge_configurations([None] * len(bridges), 0, {})

# Apply the solved bridge configurations to the grid
for index, value in zip(bridges, values):
    if value > 0:
        for row, col in product(index[2], index[3]):
            grid[row][col] = [['|', '$'][value - 1], ['-', '='][value - 1]][index[4]]

# Output the solved grid
for row in grid:
    for cell in row:
        if not cell:
            cell = [' ']
        sys.stdout.write(cell[0])
    print("")
