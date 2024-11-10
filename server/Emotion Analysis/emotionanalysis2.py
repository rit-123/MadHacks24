import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

class EmotionDetector:
    def __init__(self, model_path):
        # Load the pre-trained model
        self.model = load_model(model_path)
        
        # Initialize the webcam
        self.cap = cv2.VideoCapture(0)
        
        # Define emotion labels
        self.emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        
        # Load face cascade classifier
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Window names
        self.main_window = 'Emotion Detection (Press SPACE to capture, Q to quit)'
        self.face_window = 'Detected Face'

    def preprocess_face(self, face_img):
        # Convert to grayscale if not already
        if len(face_img.shape) == 3:
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            
        # Add padding to make it square while maintaining the face center
        height, width = face_img.shape
        size = max(height, width)
        pad_h = (size - height) // 2
        pad_w = (size - width) // 2
        
        # Create a black square image
        square_face = np.zeros((size, size), dtype=np.uint8)
        
        # Place the face in the center
        square_face[pad_h:pad_h+height, pad_w:pad_w+width] = face_img
        
        # Resize to model input size (48x48)
        face_img = cv2.resize(square_face, (48, 48))
        
        # Normalize and reshape for model input
        face_img = face_img / 255.0
        face_img = face_img.reshape(1, 48, 48, 1)
        return face_img, square_face

    def predict_emotion(self, face_img):
        # Make prediction
        prediction = self.model.predict(face_img, verbose=0)
        emotion_idx = np.argmax(prediction)
        confidence = np.max(prediction) * 100
        return self.emotion_labels[emotion_idx], confidence

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            # Create a copy of the frame for drawing
            display_frame = frame.copy()

            # Draw rectangle around each face
            for (x, y, w, h) in faces:
                # Draw rectangle
                cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Show guidelines
            cv2.putText(display_frame, 'Press SPACE to analyze emotion', 
                      (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                      1, (0, 255, 0), 2)

            # Display the frame
            cv2.imshow(self.main_window, display_frame)

            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            # Press 'q' to quit
            if key == ord('q'):
                break
                
            # Press SPACE to capture and analyze
            elif key == ord(' '):
                if len(faces) > 0:
                    # Get the largest face
                    largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
                    x, y, w, h = largest_face
                    
                    # Add a small margin around the face (20%)
                    margin = int(0.2 * min(w, h))
                    x1 = max(x - margin, 0)
                    y1 = max(y - margin, 0)
                    x2 = min(x + w + margin, frame.shape[1])
                    y2 = min(y + h + margin, frame.shape[0])
                    
                    # Extract face with margin
                    face_roi = gray[y1:y2, x1:x2]
                    
                    # Preprocess face
                    processed_face, square_face = self.preprocess_face(face_roi)
                    
                    # Get prediction
                    emotion, confidence = self.predict_emotion(processed_face)
                    
                    # Show the processed face
                    cv2.imshow(self.face_window, cv2.resize(square_face, (200, 200)))
                    
                    # Draw result on frame
                    result_text = f'{emotion} ({confidence:.1f}%)'
                    cv2.putText(display_frame, result_text, 
                              (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 
                              0.9, (0, 255, 0), 2)
                    
                    # Show the result
                    cv2.imshow(self.main_window, display_frame)
                    cv2.waitKey(2000)  # Show result for 2 seconds
                else:
                    print("No face detected! Please ensure your face is visible.")

        # Clean up
        self.cap.release()
        cv2.destroyAllWindows()

# Usage example:
if __name__ == "__main__":
    detector = EmotionDetector('facialemotionmodel.h5')
    detector.run()