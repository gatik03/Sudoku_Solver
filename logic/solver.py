class SudokuSolver:
    def __init__(self, board):
        # board should be 9x9 with 0 as empty
        self.board = board

    def is_valid(self, row, col, num):
        # Check row
        if num in self.board[row]:
            return False

        # Check column
        for i in range(9):
            if self.board[i][col] == num:
                return False

        # Check 3x3 box
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False

        return True

    def solve(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:

                    for num in range(1, 10):
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num

                            if self.solve():
                                return True

                            self.board[row][col] = 0

                    return False
        return True

    def count_solutions(self):
        count = [0]

        def backtrack():
            for row in range(9):
                for col in range(9):
                    if self.board[row][col] == 0:

                        for num in range(1, 10):
                            if self.is_valid(row, col, num):
                                self.board[row][col] = num
                                backtrack()
                                self.board[row][col] = 0

                        return

            count[0] += 1

        backtrack()
        return count[0]