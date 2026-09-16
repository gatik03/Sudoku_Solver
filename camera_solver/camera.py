import cv2

def capture_frame():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot access camera")
        return None

    # Warm up camera (important)
    for _ in range(10):
        ret, frame = cap.read()
        if not ret:
            cap.release()
            return None

    # Capture one stable frame
    ret, frame = cap.read()

    cap.release()

    if not ret:
        return None

    return frame