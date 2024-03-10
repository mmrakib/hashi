class HashiSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.rows = len(puzzle)
        self.cols = len(puzzle[0])
        self.solution = [list(row) for row in puzzle]

    def solve_puzzle(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.puzzle[row][col].isdigit():
                    island_value = int(self.puzzle[row][col])
                    self.dfs((row, col), island_value)
        return self.solution

    def dfs(self, current_island, remaining_bridges):
        row, col = current_island

        # Base case: All required bridges connected
        if remaining_bridges == 0:
            return

        # Explore neighboring islands
        for neighbor in self.get_neighbors(current_island):
            if self.solution[neighbor[0]][neighbor[1]].isdigit() or self.solution[neighbor[0]][neighbor[1]] == '.':
                # Valid connection
                self.solution[row][col] = str(int(self.solution[row][col]) + 1)
                self.solution[neighbor[0]][neighbor[1]] = str(int(self.solution[neighbor[0]][neighbor[1]]) + 1)

                # Recursive call to explore further
                self.dfs(neighbor, remaining_bridges - 1)

    def get_neighbors(self, current_island):
        row, col = current_island
        neighbors = []

        for i, j in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
            if 0 <= i < self.rows and 0 <= j < self.cols and self.puzzle[i][j].isdigit():
                neighbors.append((i, j))

        return neighbors


# Example usage:
puzzle_input = [
    ".1...6...7....4.4.2.",
    "..4.2..2...3.8...6.2",
    ".....2..............",
    "5.c.7..a.a..5.6..8.5",
    ".............2......",
    "...5...9.a..8.b.8.4.",
    "4.5................3",
    "....2..4..1.5...2...",
    ".2.7.4...7.2..5...3.",
    "............4..3.1.2"
]

hashi_solver = HashiSolver(puzzle_input)
solution = hashi_solver.solve_puzzle()

# Print the solution
for row in solution:
    print("".join(row))
