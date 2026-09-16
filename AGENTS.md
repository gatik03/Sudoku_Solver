# Developer & Agent Guidelines — Sudoku Solver & Vision Scanner

## Project Overview
**Sudoku Solver** is a desktop puzzle game and automated computer-vision solver built with Python, PyQt5, and OpenCV. It can generate boards of varying difficulty, solve any valid 9x9 board via backtracking, scan puzzles live from a webcam, or import photos of printed puzzles.

## Architecture & Directory Conventions
- `main.py`: Entrypoint launching `gui.app.run_app()`.
- `gui/app.py`:
  - `SudokuApp`: Main window containing the 9x9 interactive `QLineEdit` grid, difficulty buttons (`Easy`, `Medium`, `Hard`), solver triggers, mistake counting (`Mistakes: X/3`), and visual feedback styling.
  - `DetectionPreviewDialog`: Modal dialog showing detected numbers and confidences after photo import, highlighting low-confidence cells in red to allow human verification before populating the board.
- `logic/`:
  - `solver.py`: `SudokuSolver` backtracking algorithm. Includes `solve()` and `count_solutions()`.
  - `generator.py`: Generates complete randomized valid boards and removes numbers to produce playable puzzles.
  - `grid_detector.py`: Uses adaptive thresholding and 4-point perspective transform to extract the 9x9 bounding box from an image.
  - `digit_classifier.py`: Preprocesses extracted cell sub-images and infers the digit.
  - `photo_importer.py`: Coordinates the full pipeline from raw image file to 9x9 numeric array.
- `camera_solver/`:
  - Real-time webcam acquisition loop (`camera.py`), live contour bounding box detection (`grid_detector.py`), cell grid slicing (`cell_extractor.py`), digit inference (`digit_recognizer.py`), and unified pipeline (`pipeline.py`).
- `tests/`: Unit test suite using standard library `unittest`.

## Running & Testing
```bash
# Activate virtual environment
source venv/bin/activate

# Launch PyQt5 desktop GUI
python main.py

# Run unit tests
python -m unittest discover tests

# Check Python syntax across all modules
python -m py_compile main.py gui/app.py logic/*.py camera_solver/*.py
```

## Important Constraints for AI Agents
1. **Desktop Display Requirement**: `gui/app.py` requires an active desktop display server (`$DISPLAY` or Wayland). When running in headless environments or CI, do not execute `main.py` directly; execute `python -m unittest discover tests` instead.
2. **OpenCV Dependencies**: Computer vision routines in `logic/grid_detector.py` and `camera_solver/grid_detector.py` rely on OpenCV contour finding (`cv2.findContours`) and perspective transformation (`cv2.warpPerspective`). Ensure cell slices are strictly normalized to square dimensions before feeding to the classifier.
3. **Backtracking State Preservation**: In `logic/solver.py`, the solver modifies board states in place during recursion. Keep defensive copies (`[row[:] for row in board]`) if the original board state needs preservation.
4. **Virtual Environment**: Keep large dependencies like TensorFlow and PyQt5 inside `venv/` (which is excluded by `.gitignore`).
