from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
from typing import Tuple, List, Optional, Dict, Union
import logging
from pathlib import Path
import numpy as np

class ImageMoodClassifier:
    """A class to classify images into music mood categories using CLIP model."""
    
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        """Initialize the classifier with a CLIP model."""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Mood mapping to music adjectives
        self.mood_mappings = {
            'positive': {
                'moods': ['happy', 'surprise', 'energetic'],
                'adjectives': ['uplifting', 'positive', 'energizing', 'motivating', 'inspiring']
            },
            'calming': {
                'moods': ['sad', 'disgust', 'neutral', 'fear', 'angry'],
                'adjectives': ['calm', 'peaceful', 'quiet', 'tranquil', 'gentle']
            }
        }
        
        # Base activities without adjectives
        self.base_activities = [
            # Study/Focus
            "music for studying",
            "music for concentration",
            "music for productive work",
            "music for academic focus",
            "music for mental clarity",
            
            # Gaming
            "gaming music",
            "gaming soundtrack",
            "gaming battle music",
            "electronic gaming mix",
            "adventure gaming music",
            
            # Chill/Relax
            "lofi beats",
            "ambient music",
            "nature sounds with music",
            "meditation soundtrack",
            "acoustic relaxation",
            
            # Social
            "party music",
            "tropical house music",
            "pop music for gatherings",
            "dance music playlist",
            "social party mix",
            
            # Ambient
            "ambient soundscape",
            "atmospheric background",
            "meditation music",
            "space ambient sounds",
            "ambient drone music",
            
            # Reading
            "music for reading",
            "instrumental reading music",
            "reading soundtrack",
            "piano music for books",
            "reading atmosphere"
        ]
        
        try:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.logger.info(f"Using device: {self.device}")
            
            self.model = CLIPModel.from_pretrained(model_name).to(self.device)
            self.processor = CLIPProcessor.from_pretrained(model_name)
            self.model.eval()
            
        except Exception as e:
            self.logger.error(f"Error initializing model: {str(e)}")
            raise

    def get_mood_category(self, detected_mood: str) -> str:
        """Determine whether the mood falls into 'positive' or 'calming' category."""
        for category, mapping in self.mood_mappings.items():
            if detected_mood.lower() in mapping['moods']:
                return category
        return 'calming'  # default to calming if mood not found

    def generate_mood_specific_activities(self, detected_mood: str) -> List[str]:
        """Generate activity descriptions with mood-appropriate adjectives."""
        mood_category = self.get_mood_category(detected_mood)
        adjectives = self.mood_mappings[mood_category]['adjectives']
        
        mood_activities = []
        for base_activity in self.base_activities:
            # Randomly select an adjective for variety
            adjective = np.random.choice(adjectives)
            mood_activities.append(f"{adjective} {base_activity}")
        
        return mood_activities

    def get_top_n_predictions(self, probs: torch.Tensor, activities: List[str], n: int = 5) -> List[Tuple[str, float]]:
        """Get top N predictions with their confidence scores."""
        top_probs, top_indices = torch.topk(probs, k=min(n, len(activities)))
        return [(activities[idx], prob.item() * 100) 
                for idx, prob in zip(top_indices[0], top_probs[0])]

    @torch.no_grad()
    def classify(self, image: Union[str, Image.Image], detected_mood: str, top_n: int = 5) -> Optional[List[Tuple[str, float]]]:
        """Classify an image and return top N mood predictions with confidence scores.
        
        Args:
            image: Either a path to an image file (str) or a PIL Image object
            detected_mood (str): Detected mood from emotion analysis
            top_n (int): Number of top predictions to return
            
        Returns:
            Optional[List[Tuple[str, float]]]: List of (mood, confidence) pairs or None if classification fails
        """
        try:
            # Handle both string paths and PIL Images
            if isinstance(image, str):
                try:
                    path = Path(image)
                    if not path.exists():
                        raise FileNotFoundError(f"Image file not found: {image}")
                    image = Image.open(path).convert('RGB')
                except Exception as e:
                    self.logger.error(f"Error loading image from path: {str(e)}")
                    return None
            elif not isinstance(image, Image.Image):
                raise ValueError("Image must be either a file path or a PIL Image object")

            # Generate mood-specific activities
            mood_activities = self.generate_mood_specific_activities(detected_mood)
            
            # Prepare inputs
            inputs = self.processor(
                text=mood_activities,
                images=image,
                return_tensors="pt",
                padding=True
            )
            
            # Move inputs to the same device as model
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get prediction
            outputs = self.model(**inputs)
            probs = outputs.logits_per_image.softmax(dim=1)
            
            return self.get_top_n_predictions(probs, mood_activities, top_n)
            
        except Exception as e:
            self.logger.error(f"Error during classification: {str(e)}")
            return None

def main():
    """Main function to demonstrate the classifier usage."""
    classifier = ImageMoodClassifier()
    
    # Example usage with both file path and PIL Image
    test_cases = [
        ("study.jpg", "happy"),
        ("gaming.jpg", "energetic"),
    ]
    
    # Test with file path
    for image_path, mood in test_cases:
        try:
            predictions = classifier.classify(image_path, mood)
            if predictions:
                print(f"\nTop 5 music recommendations for {image_path} (Mood: {mood}):")
                for music_type, confidence in predictions:
                    print(f"- {music_type}: {confidence:.2f}%")
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
    
    # Test with PIL Image
    try:
        test_image = Image.open("test.jpg").convert('RGB')
        predictions = classifier.classify(test_image, "happy")
        if predictions:
            print(f"\nTop 5 music recommendations for PIL Image (Mood: happy):")
            for music_type, confidence in predictions:
                print(f"- {music_type}: {confidence:.2f}%")
    except Exception as e:
        print(f"Error processing PIL Image: {str(e)}")

if __name__ == "__main__":
    main()