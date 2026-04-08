from generator import SudokuGenerator
from solver import SudokuSolver

gen = SudokuGenerator()

# Step 1: Generate full board
full = gen.generate_full_board()

# Step 2: Create puzzle with uniqueness check
puzzle = gen.remove_numbers(clues=30)

print("PUZZLE:")
for row in puzzle:
    print(row)

# Step 3: Test uniqueness
solver = SudokuSolver([row[:] for row in puzzle])
solutions = solver.count_solutions()

print("\nNumber of solutions:", solutions)