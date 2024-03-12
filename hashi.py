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

class GraphNode:
    def __init__(self, n, x, y):
        self.n = n
        self.x = x
        self.y = y

    def __str__(self):
        return f'(n = {self.n}, x = {self.x}, y = {self.y})'

class Graph:
    def __init__(self, m):
        self.m = m
        self.nodes = []
        text = self.m.get_text()
        for i, line in enumerate(text):
            for j, ch in enumerate(line):
                n = ord(ch)
                if (ch == '.'):
                    continue
                if (n >= 48 and n <= 57):
                    node = GraphNode(n - 48, i, j)
                    self.nodes.append(node)
                if (n >= 97 and n <= 122):
                    node = GraphNode(n - 87, i, j)
                    self.nodes.append(node)
    
    def print_graph(self):
        print('Graph:')
        for node in self.nodes:
            print(node)

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

        self.text = text
        self.nrows = len(text)
        self.ncols = len(text[0])

    def get_text(self):
        return self.text
    
    def get_nrows(self):
        return self.nrows
    
    def get_ncols(self):
        return self.ncols

    def print_map(self):
        print('Map:')
        for row in self.text:
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
        graph = Graph(map)
        map.print_map()
        graph.print_graph()
    elif len(sys.argv) == 1:
        map = Map()
        graph = Graph(map)
        map.print_map()
        graph.print_graph()
    else:
        print_usage()
        exit(1)
