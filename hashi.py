#!/usr/bin/python3

# COMP3411 - Assignment 1 - 24T1
# Mohammad M. Rakib (z5361151)
#
# USAGE:
# ./hashi.py <filename>
# OR
# ./hashi.py
# Input:
# <mapdata>

import sys

class Map:
    def __init__(self, filename=''):
        text = []
        if (filename != ''):
            with open(filename, 'r') as f:
                row = []
                while True:
                    ch = f.read(1)
                    if (ch == '\n'):
                        text.append(row)
                        row = []
                        continue
                    if not ch:
                        break
                    row.append(ch)
        else:
            for line in sys.stdin:
                row = []
                for ch in line:
                    if (ch == '\n'):
                        continue
                    if not ch:
                        break
                    row.append(ch)
                text.append(row)

        self.raw = text
        self.nrows = len(text)
        self.ncols = len(text[0])

    def print_raw(self):
        for row in self.raw:
            for i, col in enumerate(row):
                if (i == len(row) - 1):
                    print(col)
                else:
                    print(col, end='')

def print_usage():
    print('hashi.py (By Mohammad M. Rakib, z5361151)\n')
    print('USAGE:')
    print('./hashi.py <filename>')
    print('OR')
    print('./hashi.py')
    print('Please enter input:')
    print('<mapdata>')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        map = Map(filename)
    elif len(sys.argv) == 1:
        map = Map()
    else:
        print_usage()
        exit(1)
