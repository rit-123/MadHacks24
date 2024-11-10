import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the model globally to avoid reloading it for each prediction
try:
    MODEL = load_model("facialemotionmodel.h5")
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    MODEL = None

def predict_emotion(image):
    """
    Predict emotion from a PIL Image using the pre-trained model.
    
    Args:
        image (PIL.Image): Input image containing a face
        
    Returns:
        tuple: (emotion_label, confidence_percentage)
        or None if no face is detected
    """
    try:
        logger.info("Starting emotion prediction")
        
        if MODEL is None:
            logger.error("Model not loaded")
            return None
            
        # Define emotion labels
        emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        
        # Load face cascade classifier
        try:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            if face_cascade.empty():
                logger.error("Failed to load face cascade classifier")
                return None
        except Exception as e:
            logger.error(f"Error loading cascade classifier: {str(e)}")
            return None
        
        # Convert PIL image to cv2 format
        try:
            cv2_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
            logger.info("Image converted successfully")
        except Exception as e:
            logger.error(f"Error converting image: {str(e)}")
            return None
        
        # Detect faces
        try:
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            logger.info(f"Detected {len(faces)} faces")
        except Exception as e:
            logger.error(f"Error detecting faces: {str(e)}")
            return None
        
        if len(faces) == 0:
            logger.info("No faces detected in the image")
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
        
        logger.info("Making prediction")
        # Make prediction
        try:
            prediction = MODEL.predict(face_img, verbose=0)
            emotion_idx = np.argmax(prediction)
            confidence = float(np.max(prediction) * 100)
            
            logger.info(f"Prediction successful: {emotion_labels[emotion_idx]} with {confidence:.2f}% confidence")
            return emotion_labels[emotion_idx], confidence
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            return None
            
    except Exception as e:
        logger.error(f"Unexpected error in predict_emotion: {str(e)}")
        return None