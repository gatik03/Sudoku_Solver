import cv2
import numpy as np

def find_largest_contour(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    return max(contours, key=cv2.contourArea)


def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )
    return thresh


def reorder_points(pts):
    pts = pts.reshape((4,2))
    new_pts = np.zeros((4,1,2), dtype=np.int32)

    add = pts.sum(1)
    new_pts[0] = pts[np.argmin(add)]
    new_pts[3] = pts[np.argmax(add)]

    diff = np.diff(pts, axis=1)
    new_pts[1] = pts[np.argmin(diff)]
    new_pts[2] = pts[np.argmax(diff)]

    return new_pts


def warp_perspective(image, contour):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

    if len(approx) != 4:
        return None

    pts = reorder_points(approx)

    pts1 = np.float32(pts)
    pts2 = np.float32([[0,0],[450,0],[0,450],[450,450]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    warped = cv2.warpPerspective(image, matrix, (450,450))

    return warped


def get_sudoku_grid(image):
    processed = preprocess(image)
    contour = find_largest_contour(processed)

    if contour is None:
        return None

    warped = warp_perspective(image, contour)
    return warped