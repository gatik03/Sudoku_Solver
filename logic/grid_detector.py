import cv2
import numpy as np

class GridDetector:
    def __init__(self):
        pass

    def detect_grid(self, image_path):
        """
        Detect the Sudoku grid and return a warped top-down image.
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not read image file.")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Robust preprocessing for varied lighting
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)
        
        # Dilation to join broken lines
        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=1)

        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            raise ValueError("No grid detected in the image.")

        # Find largest 4-sided contour
        grid_contour = None
        max_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000: # Minimum area threshold
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                if len(approx) == 4 and area > max_area:
                    grid_contour = approx
                    max_area = area

        if grid_contour is None:
            raise ValueError("Could not find a square Sudoku grid. Ensure the grid is clearly visible.")

        # Perspective Transform
        rect = self._order_points(grid_contour.reshape(4, 2))
        (tl, tr, br, bl) = rect

        # Determine dimensions for warping
        width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        max_width = max(int(width_a), int(width_b), 450)

        height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        max_height = max(int(height_a), int(height_b), 450)

        dst = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]
        ], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(gray, M, (max_width, max_height))

        return warped

    def split_cells(self, warped_image):
        """
        Split the warped grid into 81 cells.
        """
        cells = []
        h, w = warped_image.shape
        cell_h, cell_w = h // 9, w // 9

        for r in range(9):
            for c in range(9):
                y1, y2 = r * cell_h, (r + 1) * cell_h
                x1, x2 = c * cell_w, (c + 1) * cell_w
                cell = warped_image[y1:y2, x1:x2]
                cells.append(cell)
        
        return cells

    def _order_points(self, pts):
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)] # Top-left
        rect[2] = pts[np.argmax(s)] # Bottom-right
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)] # Top-right
        rect[3] = pts[np.argmax(diff)] # Bottom-left
        return rect
