import cv2
import pytesseract

def recognize_digit(cell):
    cell = cv2.resize(cell, (100, 100))
    _, cell = cv2.threshold(cell, 150, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(
        cell,
        config='--psm 10 -c tessedit_char_whitelist=123456789'
    )

    text = text.strip()

    if text.isdigit():
        return int(text)

    return 0