from camera_solver.camera import capture_frame
from camera_solver.grid_detector import get_sudoku_grid
from camera_solver.cell_extractor import split_cells
from camera_solver.digit_recognizer import recognize_digit


def get_sudoku_from_camera():
    frame = capture_frame()

    if frame is None:
        return None

    grid = get_sudoku_grid(frame)

    if grid is None:
        print("Grid not detected")
        return None

    cells = split_cells(grid)

    board = []
    for i in range(9):
        row = []
        for j in range(9):
            digit = recognize_digit(cells[i * 9 + j])
            row.append(digit)
        board.append(row)

    return board