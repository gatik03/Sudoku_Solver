import numpy as np
import cv2

def split_cells(grid):
    grid = cv2.cvtColor(grid, cv2.COLOR_BGR2GRAY)
    rows = np.vsplit(grid, 9)

    cells = []
    for row in rows:
        cols = np.hsplit(row, 9)
        for cell in cols:
            cells.append(cell)

    return cells