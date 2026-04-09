import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit,
    QPushButton, QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator

from logic.solver import SudokuSolver
from logic.generator import SudokuGenerator


class SudokuApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sudoku Solver")
        self.setGeometry(100, 100, 600, 600)

        self.grid_cells = []
        self.solution = None
        self.original_puzzle = None
        self.mistakes = 0
        self.game_over = False

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # Create grid
        for row in range(9):
            row_cells = []
            for col in range(9):
                cell = QLineEdit()

                cell.setFixedSize(50, 50)
                cell.setAlignment(Qt.AlignCenter)
                cell.setMaxLength(1)
                cell.setValidator(QIntValidator(1, 9))

                grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)

            self.grid_cells.append(row_cells)

        # Buttons
        generate_btn = QPushButton("Generate")
        generate_btn.clicked.connect(self.generate_board)

        solve_btn = QPushButton("Solve")
        solve_btn.clicked.connect(self.solve_board)

        main_layout.addLayout(grid_layout)
        main_layout.addWidget(generate_btn)
        main_layout.addWidget(solve_btn)

        central_widget.setLayout(main_layout)

    # --------------------------
    # CORE FUNCTIONS
    # --------------------------

    def get_board(self):
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                text = self.grid_cells[row][col].text()
                current_row.append(int(text) if text else 0)
            board.append(current_row)
        return board

    def set_board(self, board):
        for row in range(9):
            for col in range(9):
                cell = self.grid_cells[row][col]

                if board[row][col] != 0:
                    cell.setText(str(board[row][col]))
                else:
                    cell.clear()

                # RESET STYLE EVERY TIME
                cell.setStyleSheet("color: black;")

    # --------------------------
    # GENERATE GAME
    # --------------------------

    def generate_board(self):
        gen = SudokuGenerator()

        puzzle = gen.generate_full_board()
        puzzle = gen.remove_numbers(clues=30)

        self.original_puzzle = [row[:] for row in puzzle]

        # Get solution
        solver = SudokuSolver([row[:] for row in puzzle])
        solver.solve()
        self.solution = solver.board

        self.mistakes = 0
        self.game_over = False

        self.set_board(puzzle)

        for row in range(9):
            for col in range(9):
                cell = self.grid_cells[row][col]

                if puzzle[row][col] != 0:
                    cell.setReadOnly(True)
                else:
                    cell.setReadOnly(False)

                    try:
                        cell.editingFinished.disconnect()
                    except:
                        pass

                    # FIXED SIGNAL
                    cell.editingFinished.connect(
                        lambda r=row, c=col: self.check_input(r, c)
                    )

        print("New Game")

    # --------------------------
    # SOLVER
    # --------------------------

    def solve_board(self):
        if not self.original_puzzle:
            return

        board = [row[:] for row in self.original_puzzle]

        solver = SudokuSolver(board)

        if solver.solve():
            self.set_board(solver.board)
        else:
            print("No solution exists")

    # --------------------------
    # GAME LOGIC
    # --------------------------

    def check_input(self, row, col):
        if self.game_over or not self.solution:
            return

        cell = self.grid_cells[row][col]
        text = cell.text()

        if not text:
            return

        value = int(text)

        # Prevent re-counting same wrong input
        if cell.styleSheet() == "color: red;":
            return

        if value != self.solution[row][col]:
            self.mistakes += 1
            cell.setStyleSheet("color: red;")

            print("Mistakes:", self.mistakes)

            if self.mistakes >= 3:
                print("Game Over!")
                self.game_over = True

                for r in range(9):
                    for c in range(9):
                        self.grid_cells[r][c].setReadOnly(True)

                return
        else:
            cell.setStyleSheet("color: green;")
            cell.setReadOnly(True)

        self.check_win()

    def check_win(self):
        if self.game_over:
            return

        for row in range(9):
            for col in range(9):
                text = self.grid_cells[row][col].text()
                if not text or int(text) != self.solution[row][col]:
                    return

        print("You solved it!")




def run_app():
    app = QApplication(sys.argv)
    window = SudokuApp()
    window.show()
    sys.exit(app.exec_())