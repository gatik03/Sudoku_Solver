import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from logic.solver import SudokuSolver
from PyQt5.QtGui import QIntValidator
from logic.generator import SudokuGenerator

class SudokuApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sudoku Solver")
        self.setGeometry(100, 100, 600, 600)

        self.grid_cells = []

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

        # Solve button
        # Buttons
        generate_btn = QPushButton("Generate")
        generate_btn.clicked.connect(self.generate_board)

        solve_btn = QPushButton("Solve")
        solve_btn.clicked.connect(self.solve_board)

        main_layout.addLayout(grid_layout)
        main_layout.addWidget(generate_btn)
        main_layout.addWidget(solve_btn)

        central_widget.setLayout(main_layout)

    def get_board(self):
        board = []

        for row in range(9):
            current_row = []
            for col in range(9):
                text = self.grid_cells[row][col].text()

                if text == "":
                    current_row.append(0)
                else:
                    current_row.append(int(text))

            board.append(current_row)

        return board
    def set_board(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] != 0:
                    self.grid_cells[row][col].setText(str(board[row][col]))
                else:
                    self.grid_cells[row][col].clear()

    def solve_board(self):
        board = self.get_board()

        solver = SudokuSolver(board)

        if solver.solve():
            self.set_board(solver.board)
        else:
            print("No solution exists")

    def generate_board(self):
        from logic.generator import SudokuGenerator  # adjust if using core/

        gen = SudokuGenerator()

        full = gen.generate_full_board()
        puzzle = gen.remove_numbers(clues=30)

        self.set_board(puzzle)

        # Lock pre-filled cells
        for row in range(9):
            for col in range(9):
                if puzzle[row][col] != 0:
                    self.grid_cells[row][col].setReadOnly(True)
                else:
                    self.grid_cells[row][col].setReadOnly(False)
                    self.grid_cells[row][col].clear()

def run_app():
    app = QApplication(sys.argv)
    window = SudokuApp()
    window.show()
    sys.exit(app.exec_())