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
import math

def error(message):
    print(f'ERROR: {message}')
    exit(1)

class GraphNode:
    def __init__(self, n, x, y):
        self.n = n
        self.nleft = n
        self.x = x
        self.y = y

    def __str__(self):
        return f'(n = {self.n}, x = {self.x}, y = {self.y})'
    
class GraphEdge:
    def __init__(self, n1, n2, numbridges):
        self.n1 = n1
        self.n2 = n2
        self.numbridges = numbridges

class Graph:
    def __init__(self, map):
        self.map = map
        self.nodes = []
        self.edges = []

        text = self.map.get_text()

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

    @staticmethod
    def calc_dist(n1, n2):
        if (n1.y == n2.y):
            return abs(n1.x - n2.x)
        elif (n1.x == n2.x):
            return abs(n1.y - n2.y)
        else:
            error('Tried to calculate diagonal distances')

    def find_neighbours(self, target):
        x_neighbours = []
        y_neighbours = []

        for node in self.nodes:
            if (target.x == node.x and target.y == node.y):
                continue
            if (target.x == node.x):
                x_neighbours.append(node)
            if (target.y == node.y):
                y_neighbours.append(node)
        
        return x_neighbours, y_neighbours

    def find_nearest_neighbours(self, target):
        x_neighbours, y_neighbours = self.find_neighbours(target)

        nearest_neighbours = {'up': None, 'down': None, 'left': None, 'right': None}
        min_dists = {'up': math.inf, 'down': math.inf, 'left': math.inf, 'right': math.inf}

        for node in x_neighbours:
            # Left
            if (node.y < target.y):
                dist = Graph.calc_dist(node, target)
                if (dist < min_dists['left']):
                    nearest_neighbours['left'] = node
                    min_dists['left'] = dist

            # Right
            if (node.y > target.y):
                dist = Graph.calc_dist(node, target)
                if (dist < min_dists['right']):
                    nearest_neighbours['right'] = node
                    min_dists['right'] = dist
        
        for node in y_neighbours:
            # Up
            if (node.x < target.x):
                dist = Graph.calc_dist(node, target)
                if (dist < min_dists['up']):
                    nearest_neighbours['up'] = node
                    min_dists['up'] = dist

            # Down
            if (node.x > target.x):
                dist = Graph.calc_dist(node, target)
                if (dist < min_dists['down']):
                    nearest_neighbours['down'] = node
                    min_dists['down'] = dist

        return nearest_neighbours
        
    def print_graph(self):
        print('Graph:')

        for node in self.nodes:
            print('current node:')
            print(node)
            nearest_neighbours = self.find_nearest_neighbours(node)

            print('nearest neighbours:')
            print(f'left: {str(nearest_neighbours['left'])}')
            print(f'right: {str(nearest_neighbours['right'])}')
            print(f'up: {str(nearest_neighbours['up'])}')
            print(f'down: {str(nearest_neighbours['down'])}')
            print('')

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
