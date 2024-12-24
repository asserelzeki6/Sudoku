import random
from utils.algorithms import solve

class Backtracking:
    def __init__(self):
        self.moves = []
        self.board = []
        self.ai_moves = []

    # for user turn by turn
    def is_valid(self, row, col, num):
        if num in self.board[row]:
            return False
        if num in [self.board[i][col] for i in range(9)]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    # when solve is pressed
    def solve_sudoku(self, randomm=False):
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty
        numbers = list(range(1, 10))
        if randomm:
            random.shuffle(numbers)
        for num in numbers:
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.solve_sudoku(randomm):
                    if not randomm:
                        self.ai_moves.append((row, col, num))
                    return True
                self.board[row][col] = 0
        return False

    # not used with front
    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    # not used with front
    def generate_full_solution(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.solve_sudoku(True)

    # when generate is pressed
    def generate_puzzle(self, mode):
        self.generate_full_solution()
        cells_to_remove = 35
        if mode == "Medium":
            cells_to_remove = 45  # hard = 55, medium = 45, easy = 35
        elif mode == "Hard":
            cells_to_remove = 55

        non_empty_cells = [(row, col) for row in range(9) for col in range(9)]
        while cells_to_remove > 0:
            if len(non_empty_cells) == 0:
                print("Too many values to remove")

            row1, col = random.choice(non_empty_cells)
            backup = self.board[row1][col]
            self.board[row1][col] = 0
            if not self.has_unique_solution():
                self.board[row1][col] = backup
            else:
                non_empty_cells.remove((row1, col))
                cells_to_remove -= 1

        # self.print_board(self.board)

    # not used with front
    def has_unique_solution(self):
        solutions = []

        def solve_with_tracking():
            if len(solutions) > 1:
                return

            empty = self.find_empty()
            if not empty:
                solutions.append([row[:] for row in self.board])
                return

            row, col = empty
            for num in range(1, 10):
                if self.is_valid(row, col, num):
                    self.board[row][col] = num
                    solve_with_tracking()
                    self.board[row][col] = 0

        solve_with_tracking()
        return len(solutions) == 1

    # for mode 2, user enter grid
    def validate_input(self, board):
        self.board = board
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    temp = self.board[i][j]
                    self.board[i][j] = 0
                    if not self.is_valid(i, j, temp):
                        return False
                    self.board[i][j] = temp
        return self.has_unique_solution()

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) if num != 0 else '.' for num in row))
        print()

if __name__ == "__main__":
    sudoku_solver = Backtracking()
    puzzle = [[1, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    sudoku_solver.generate_puzzle("Easy")
    sudoku_solver.print_board()
    # print("Validating input puzzle:")
    print(sudoku_solver.validate_input(puzzle))
    #
    # print("Solving the puzzle:")
    # sudoku_solver.solve_sudoku(False)

    # Sudoku solver using backtracking and forward checking algorithm
    assignment = {}
    solve(puzzle, assignment, True)
    moves = [(key[0], key[1], value) for key, value in assignment.items()]
    print(moves)
    sudoku_solver.board = puzzle
    sudoku_solver.ai_moves = moves
    ##################################################################
    
    # sudoku_solver.ai_moves.reverse()
    # print(sudoku_solver.ai_moves)
    # sudoku_solver.print_board()
