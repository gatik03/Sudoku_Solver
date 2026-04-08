import random
from logic.solver import SudokuSolver


class SudokuGenerator:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]

    def is_valid(self, row, col, num):
        # row
        if num in self.board[row]:
            return False

        # column
        for i in range(9):
            if self.board[i][col] == num:
                return False

        # box
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False

        return True

    def fill_board(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:

                    nums = list(range(1, 10))
                    random.shuffle(nums)

                    for num in nums:
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num

                            if self.fill_board():
                                return True

                            self.board[row][col] = 0

                    return False
        return True

    def generate_full_board(self):
        self.fill_board()
        return self.board

    def remove_numbers(self, clues=30):
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)

        removed = 81 - clues

        count = 0

        for row, col in cells:
            if count >= removed:
                break

            backup = self.board[row][col]
            self.board[row][col] = 0

            # check uniqueness
            solver = SudokuSolver([row[:] for row in self.board])
            solutions = solver.count_solutions()

            if solutions != 1:
                # revert
                self.board[row][col] = backup
            else:
                count += 1

        return self.board
