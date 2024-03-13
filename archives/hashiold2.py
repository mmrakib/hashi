#!/usr/bin/python3

import sys
from itertools import product, combinations
from pprint import pprint

def load_grid():
    grid = []
    for row, line in (enumerate(open(sys.argv[1])) if len(sys.argv) == 2 else enumerate(sys.stdin)):
        rowlist = []
        for col, cell in enumerate(line.strip()):
            if (cell != '.'):
                rowlist.append((row, col, cell, []))
            else:
                rowlist.append(0)
        grid.append(rowlist)
    nrows = len(grid)
    ncols = len(grid[0])
    return grid, nrows, ncols

def generate_bridge_configurations(grid, nrows, ncols):
    bridges = []
    for point1, point2 in combinations(product(range(nrows), range(ncols)), 2):
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
    return bridges

def print_grid(grid):
    for row in grid:
        for cell in row:
            if not cell:
                print('.', end='')
            else:
                print(cell[2], end='')
        print('')

if __name__ == '__main__':
    grid, nrows, ncols = load_grid()
    print_grid(grid)
    bridges = generate_bridge_configurations(grid, nrows, ncols)
    for b in bridges:
        print(b)
