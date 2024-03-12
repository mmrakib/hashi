#!/usr/bin/python3

import sys

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
    return grid

def print_grid(grid):
    for row in grid:
        for cell in row:
            if not cell:
                print('.', end='')
            else:
                print(cell[2], end='')
        print('')

if __name__ == '__main__':
    grid = load_grid()
    print_grid(grid)
