from .grid_detector import GridDetector
from .digit_classifier import SudokuDigitClassifier

class ImageToSudoku:
    def __init__(self):
        self.detector = GridDetector()
        self.classifier = SudokuDigitClassifier()

    def process_image(self, image_path):
        """
        Processes image using robust detection and DL classification.
        """
        # 1. Detect Grid
        warped = self.detector.detect_grid(image_path)
        
        # 2. Split into 81 cells
        cells = self.detector.split_cells(warped)
        
        # 3. Classify each cell
        grid = [[0 for _ in range(9)] for _ in range(9)]
        confidences = [[100.0 for _ in range(9)] for _ in range(9)] # Default high confidence for DL

        for i, cell in enumerate(cells):
            row, col = divmod(i, 9)
            digit = self.classifier.predict_digit(cell)
            grid[row][col] = digit
            
        return grid, confidences
