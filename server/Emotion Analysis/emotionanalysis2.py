import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model

model_path = "facialemotionmodel.h5"

def predict_emotion(image):
    """
    Predict emotion from a PIL Image using the pre-trained model.
    
    Args:
        image (PIL.Image): Input image containing a face
        model_path (str): Path to the trained emotion detection model
        
    Returns:
        tuple: (emotion_label, confidence_percentage)
        or None if no face is detected
    """
    # Load the model
    model = load_model(model_path)
    
    # Define emotion labels (same as original)
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    
    # Load face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Convert PIL image to cv2 format
    cv2_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    if len(faces) == 0:
        return None
    
    # Get the largest face
    largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
    x, y, w, h = largest_face
    
    # Add margin around the face (20%)
    margin = int(0.2 * min(w, h))
    x1 = max(x - margin, 0)
    y1 = max(y - margin, 0)
    x2 = min(x + w + margin, gray.shape[1])
    y2 = min(y + h + margin, gray.shape[0])
    
    # Extract face ROI
    face_roi = gray[y1:y2, x1:x2]
    
    # Make the image square while maintaining the face center
    height, width = face_roi.shape
    size = max(height, width)
    pad_h = (size - height) // 2
    pad_w = (size - width) // 2
    
    # Create a black square image
    square_face = np.zeros((size, size), dtype=np.uint8)
    
    # Place the face in the center
    square_face[pad_h:pad_h+height, pad_w:pad_w+width] = face_roi
    
    # Resize to model input size (48x48)
    face_img = cv2.resize(square_face, (48, 48))
    
    # Normalize and reshape for model input
    face_img = face_img / 255.0
    face_img = face_img.reshape(1, 48, 48, 1)
    
    # Make prediction
    prediction = model.predict(face_img, verbose=0)
    emotion_idx = np.argmax(prediction)
    confidence = float(np.max(prediction) * 100)
    
    return emotion_labels[emotion_idx], confidence


# Load a sample image
image_path = "test.jpg"
image = Image.open(image_path)

# Predict emotion
result = predict_emotion(image)

if result:
    emotion_label, confidence = result
    print(f"Emotion: {emotion_label}, Confidence: {confidence:.2f}%")
else:
    print("No face detected in the image.")