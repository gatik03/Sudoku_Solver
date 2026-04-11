import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit,
    QPushButton, QVBoxLayout, QLabel
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

        self.selected_cell = None
        self.selected_row = None
        self.selected_col = None

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        self.mistake_label = QLabel("Mistakes: 0/3")
        self.mistake_label.setStyleSheet("color: white; font-size: 16px;")

        main_layout.addWidget(self.mistake_label)


        # Create grid
        for row in range(9):
            row_cells = []
            for col in range(9):
                cell = QLineEdit()

                cell.setFixedSize(60, 60)
                cell.setAlignment(Qt.AlignCenter)
                cell.setMaxLength(1)
                cell.setValidator(QIntValidator(1, 9))
                style = ""

                if col % 3 == 0:
                    style += "border-left: 2px solid white;"

                if row % 3 == 0:
                    style += "border-top: 2px solid white;"

                # Optional: right & bottom borders for outer edges
                if col == 8:
                    style += "border-right: 2px solid white;"
                if row == 8:
                    style += "border-bottom: 2px solid white;"

               

                cell.mousePressEvent = lambda event, r=row, c=col: self.select_cell(self.grid_cells[r][c], r, c)


                grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)

            self.grid_cells.append(row_cells)


        num_layout = QGridLayout()

        for i in range(9):
            btn = QPushButton(str(i+1))
            btn.setFixedSize(50, 50)
            btn.clicked.connect(lambda _, n=i+1: self.fill_selected(n))
            num_layout.addWidget(btn, 0, i)
      
        main_layout.addLayout(num_layout)

        # Buttons
        easy_btn = QPushButton("Easy")
        medium_btn = QPushButton("Medium")
        hard_btn = QPushButton("Hard")

        easy_btn.clicked.connect(lambda: self.generate_board(40))
        medium_btn.clicked.connect(lambda: self.generate_board(34))
        hard_btn.clicked.connect(lambda: self.generate_board(28))

        main_layout.addWidget(easy_btn)
        main_layout.addWidget(medium_btn)
        main_layout.addWidget(hard_btn)

        solve_btn = QPushButton("Solve")
        solve_btn.clicked.connect(self.solve_board)

        main_layout.addLayout(grid_layout)
        main_layout.addWidget(solve_btn)

        central_widget.setLayout(main_layout)

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
                cell.setStyleSheet("color: white;")

    def update_styles(self):
        for row in range(9):
            for col in range(9):
                cell = self.grid_cells[row][col]

                style = ""

                bg = "#1a1f35"

                if self.selected_row is not None:
                    if row == self.selected_row or col == self.selected_col:
                        bg = "#2a2f4a"

                    if row == self.selected_row and col == self.selected_col:
                        bg = "#3a4170"

                style += f"background-color: {bg};"

                text_color = "#e0e6ff"

                if cell.text():
                    if self.solution:
                        if int(cell.text()) == self.solution[row][col]:
                            text_color = "#4CAF50"
                        else:
                            text_color = "#ff4d4d"

                style += f"color: {text_color};"

                style += "border: 1px solid #2a2f4a;"

                if col % 3 == 0:
                    style += "border-left: 3px solid white;"
                if row % 3 == 0:
                    style += "border-top: 3px solid white;"
                if col == 8:
                    style += "border-right: 3px solid white;"
                if row == 8:
                    style += "border-bottom: 3px solid white;"

                cell.setStyleSheet(style)
    def generate_board(self, clues=30):
        gen = SudokuGenerator()

        puzzle = gen.generate_full_board()
        puzzle = gen.remove_numbers(clues=clues)

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
        self.update_styles()
        print("New Game")

    def solve_board(self):
        if not self.original_puzzle:
            return

        board = [row[:] for row in self.original_puzzle]

        solver = SudokuSolver(board)

        if solver.solve():
            self.set_board(solver.board)
        else:
            print("No solution exists")

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

            self.mistake_label.setText(f"Mistakes: {self.mistakes}/3")

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
        self.update_styles()

    def check_win(self):
        if self.game_over:
            return

        for row in range(9):
            for col in range(9):
                text = self.grid_cells[row][col].text()
                if not text or int(text) != self.solution[row][col]:
                    return

        print("You solved it!")

    def fill_selected(self, number):
        if hasattr(self, "selected_cell") and self.selected_cell:
            self.selected_cell.setText(str(number))
    def select_cell(self, cell,row,col):
            self.selected_cell = cell
            self.selected_row = row
            self.selected_col = col
            self.update_styles()
    
def run_app():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow {
            background-color: #0f1220;
        }

        QLineEdit {
            background-color: #1a1f35;
            color: #e0e6ff;
            font-size: 18px;
            border: 1px solid #2a2f4a;
        }

        QLineEdit:focus {
            border: 2px solid #4a90ff;
            background-color: #232a4d;
        }

        QPushButton {
            background-color: #2a2f4a;
            color: white;
            font-size: 14px;
            padding: 8px;
            border-radius: 6px;
        }

        QPushButton:hover {
            background-color: #3a4170;
        }
    """)

    window = SudokuApp()
    window.show()
    sys.exit(app.exec_())