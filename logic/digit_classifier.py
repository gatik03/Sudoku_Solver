import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

class SudokuDigitClassifier:
    def __init__(self, model_path='sudoku_model.h5'):
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self):
        """
        Loads the pre-trained CNN model. If it doesn't exist, builds a basic one.
        """
        if os.path.exists(self.model_path):
            try:
                return models.load_model(self.model_path)
            except Exception as e:
                print(f"Error loading model: {e}")
        
        # Define CNN architecture (MNIST style)
        model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(10, activation='softmax') # 0-9
        ])
        
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        
        print("Warning: Pre-trained model not found. Using an untrained model architecture.")
        return model

    def preprocess_image(self, cell_image):
        """
        Preprocess a single cell image for prediction.
        """
        # Convert to grayscale if not already
        if len(cell_image.shape) == 3:
            gray = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = cell_image

        # Resize to 28x28
        resized = cv2.resize(gray, (28, 28), interpolation=cv2.INTER_AREA)

        # Threshold and normalize
        _, thresh = cv2.threshold(resized, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Normalize to [0, 1]
        normalized = thresh.astype('float32') / 255.0
        
        # Reshape for model input
        return normalized.reshape(1, 28, 28, 1)

    def predict_digit(self, cell_image):
        """
        Predict the digit in the cell image.
        Returns: 0-9 (0 for empty or non-digit).
        """
        processed = self.preprocess_image(cell_image)
        
        # Check if cell is empty by pixel density
        if np.mean(processed) < 0.03: # Very few white pixels
            return 0

        prediction = self.model.predict(processed, verbose=0)
        digit = np.argmax(prediction)
        confidence = np.max(prediction)

        # If confidence is too low, treat as empty
        if confidence < 0.6:
            return 0
            
        return int(digit)
