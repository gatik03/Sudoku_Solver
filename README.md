# Sudoku Solver & Vision Scanner

A desktop Sudoku application featuring an interactive PyQt5 interface, backtracking solver engine, puzzle generator with difficulty presets, and computer-vision-based puzzle recognition from static photos and live webcams.

## Features

- **Interactive GUI:** Built with PyQt5, providing cell inputs, digit keypad, mistake counters (up to 3 mistakes before game over), and live verification.
- **Difficulty Presets:** Generate playable boards on the fly:
  - Easy (40 clues)
  - Medium (34 clues)
  - Hard (28 clues)
- **Automatic Solver:** Instant solution backtracking algorithm (`logic/solver.py`) capable of finding valid solutions and counting solution uniqueness.
- **Photo Import:** Load Sudoku puzzles from PNG/JPG/JPEG images (`logic/photo_importer.py`). Uses OpenCV contour detection, perspective unwarping, and digit classification, with a pre-solve confirmation dialog for low-confidence cells.
- **Live Camera Scanner:** Real-time webcam frame acquisition and perspective grid extraction (`camera_solver/`).

## Tech Stack

- **GUI:** PyQt5
- **Computer Vision:** OpenCV (`opencv-python-headless` or `opencv-python`)
- **Image Processing & ML:** NumPy, Pillow, scikit-image, Tesseract OCR (`pytesseract`), TensorFlow
- **Test Runner:** Python standard library `unittest`

## Project Structure

```text
sudoku_solver/
├── camera_solver/           # Real-time webcam vision pipeline
│   ├── camera.py            # Video capture stream handler
│   ├── cell_extractor.py    # 9x9 bounding box slicing
│   ├── digit_recognizer.py  # Digit inference
│   ├── grid_detector.py     # Contour discovery & perspective warp
│   └── pipeline.py          # Unified camera-to-board pipeline
├── gui/
│   ├── __init__.py
│   └── app.py               # PyQt5 GUI, SudokuApp, and DetectionPreviewDialog
├── logic/
│   ├── __init__.py
│   ├── digit_classifier.py  # Image OCR / CNN classifier
│   ├── generator.py         # Full board creation and clue removal
│   ├── grid_detector.py     # Image-based grid detection and rectification
│   ├── photo_importer.py    # High-level photo to grid coordinator
│   ├── solver.py            # Backtracking solver and uniqueness checker
│   └── test.py              # CLI test script
├── tests/
│   ├── __init__.py
│   └── test_solver.py       # Automated unit tests (unittest)
├── main.py                  # Desktop application entry point
├── sudoku.py                # Standalone script demonstrating generator algorithms
├── requirements.txt         # Pinned Python package dependencies
├── .gitignore               # Ignored environments, caches, and local files
├── AGENTS.md                # AI agent and developer architectural notes
└── README.md                # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.10+ (tested on Python 3.12)
- Linux/macOS/Windows desktop with X11/Wayland display server
- (Optional for camera scanning) Connected webcam
- (Optional for OCR) `tesseract-ocr` system package installed if using Tesseract backend

### Installation

1. **Clone repository:**
   ```bash
   git clone <repository-url>
   cd sudoku_solver
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Launch the desktop GUI:
```bash
python main.py
```

### Running Unit Tests

Run the built-in test suite:
```bash
python -m unittest discover tests
```

## Developer & Agent Guidelines

For architectural details, computer vision constraints, and GUI signal patterns, refer to [AGENTS.md](AGENTS.md).

## License

MIT License.
