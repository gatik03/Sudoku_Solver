import numpy as np 
import random
a=[]
"""
def sudoku_generator(arr, diff):
	arr = [[1]*9 for i in range(9)]
	for j in range (9):
		for i in range(9):
			arr[j][i]= random.randint(1,9)

	return arr
print (sudoku_generator(a,1))

"""

import random

def is_valid(board, row, col, num):
    # row
    if num in board[row]:
        return False

    # column
    for i in range(9):
        if board[i][col] == num:
            return False

    # 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3

    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True


def fill_board(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:

                nums = list(range(1, 10))
                random.shuffle(nums)

                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num

                        if fill_board(board):
                            return True

                        board[row][col] = 0

                return False
    return True


def generate_full_board():
    board = [[0]*9 for _ in range(9)]
    fill_board(board)
    return board


board = generate_full_board()

for row in board:
    print(row)

print('')


def remove_numbers(board, clues=30):
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)

    removed = 81 - clues

    for i in range(removed):
        row, col = cells[i]
        board[row][col] = 0

    return board

board = (remove_numbers(board, 50))
for row in board:
	print (row)

