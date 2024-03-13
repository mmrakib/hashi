import sys
from itertools import product, combinations

def read_puzzle(filename):
    puzzle = []
    with open(filename, 'r') as file:
        for row, line in enumerate(file):
            puzzle_row = []
            for col, char in enumerate(line.strip()):
                if char != '.':
                    puzzle_row.append((char, row, col))
                else:
                    puzzle_row.append(None)
            puzzle.append(puzzle_row)
    return puzzle

def find_connections(puzzle):
    connections = []
    rows = range(len(puzzle))
    cols = range(len(puzzle[0]))
    for (row1, col1), (row2, col2) in combinations(product(rows, cols), 2):
        if puzzle[row1][col1] and puzzle[row2][col2]:
            if row1 == row2 and abs(col1 - col2) > 1:
                if not any(puzzle[row1][c] for c in range(min(col1, col2) + 1, max(col1, col2))):
                    connections.append(((row1, col1), (row2, col2), [row1], range(min(col1, col2) + 1, max(col1, col2)), 1))
            elif col1 == col2 and abs(row1 - row2) > 1:
                if not any(puzzle[r][col1] for r in range(min(row1, row2) + 1, max(row1, row2))):
                    connections.append(((row1, col1), (row2, col2), range(min(row1, row2) + 1, max(row1, row2)), [col1], 0))
    return connections

def solve_puzzle(puzzle, connections):
    rows = range(len(puzzle))
    cols = range(len(puzzle[0]))
    def backtrack(values, index, bridge_counts):
        if index >= len(values):
            return None
        for bridge_type in [2, 1, 0]:
            values[index] = bridge_type
            new_bridge_counts = dict(bridge_counts)
            valid = True
            for i in [0, 1]:
                node = connections[index][i]
                if node not in new_bridge_counts:
                    new_bridge_counts[node] = 0
                new_bridge_counts[node] += bridge_type
                node_value = int(connections[index][i][0])
                if new_bridge_counts[node] > node_value:
                    valid = False
                    break
            if not valid:
                continue
            active_bridges = [(d[0], d[1]) for b in range(index + 1) for d in product(connections[b][2], connections[b][3]) if values[b] > 0]
            if len(active_bridges) != len(set(active_bridges)):
                continue
            if index == len(values) - 1:
                grid_solved = True
                for row, col in product(rows, cols):
                    node = puzzle[row][col]
                    if node:
                        if new_bridge_counts[(row, col)] != int(node[0]):
                            grid_solved = False
                            break
                if grid_solved:
                    return values
            solution = backtrack(values, index + 1, new_bridge_counts)
            if solution:
                return solution
        return None

    puzzle_solution = []
    for index, value in enumerate(backtrack([None] * len(connections), 0, {})):
        if value > 0:
            for row, col in product(connections[index][2], connections[index][3]):
                puzzle[ row ][ col ] = [['|', '$'][value - 1], ['-', '='][value - 1]][connections[index][4]]
    return puzzle

def print_puzzle(puzzle):
    for row in puzzle:
        for cell in row:
            if cell:
                sys.stdout.write(cell[0])
            else:
                sys.stdout.write(' ')
        print("")

if __name__ == "__main__":
    puzzle_filename = sys.argv[1]
    puzzle_grid = read_puzzle(puzzle_filename)
    connections = find_connections(puzzle_grid)
    solved_puzzle = solve_puzzle(puzzle_grid, connections)
    print_puzzle(solved_puzzle)
