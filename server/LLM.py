from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

def classify_screenshot(image):
    # Load CLIP model and processor
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    
    # Spotify-friendly mood labels that match with activities
    activities = [
        "focus music for studying",
        "instrumental concentration",
        "gaming music playlist",
        "chill relaxing beats",
        "upbeat social music",
        "coding focus music",
        "ambient background music",
        "peaceful reading music",
        "study beats"
    ]
    
    # Load and process image
    
    if isinstance(image, str):
        image = Image.open(image)
    # Prepare inputs
    inputs = processor(
        text=activities,
        images=image,
        return_tensors="pt",
        padding=True
    )
    
    # Get prediction
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    
    # Get top prediction
    top_prob, top_idx = torch.max(probs, dim=1)
    predicted_mood = activities[top_idx.item()]
    confidence = top_prob.item() * 100
    
    return predicted_mood, confidence

# Example usage
if __name__ == "__main__":
    try:
        # Replace with your screenshot path
        image_path = "screenshot641.png"  # Update this to your image path
        
        mood, confidence = classify_screenshot(image_path)
        print(f"\nSpotify Mood Label: {mood}")
        print(f"Confidence: {confidence:.2f}%")
        
    except Exception as e:
        print(f"Error: {str(e)}")