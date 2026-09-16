import unittest
from logic.generator import SudokuGenerator
from logic.solver import SudokuSolver


class TestSudokuSolver(unittest.TestCase):
    def test_sudoku_generator_and_solver(self):
        gen = SudokuGenerator()
        full_board = gen.generate_full_board()

        # Ensure full board has no zeros
        for row in full_board:
            self.assertNotIn(0, row)
            self.assertEqual(sorted(row), list(range(1, 10)))

        # Remove numbers to create puzzle
        puzzle = gen.remove_numbers(clues=32)

        # Solve puzzle
        solver = SudokuSolver([row[:] for row in puzzle])
        self.assertTrue(solver.solve())
        self.assertGreaterEqual(solver.count_solutions(), 1)

    def test_solver_invalid_board(self):
        # Two identical numbers in the same row
        invalid_board = [
            [5, 5, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        solver = SudokuSolver(invalid_board)
        self.assertFalse(solver.is_valid(0, 2, 5))


if __name__ == "__main__":
    unittest.main()
