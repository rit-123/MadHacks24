from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
from typing import Tuple, List, Optional
import logging
from pathlib import Path
import numpy as np

class ImageMoodClassifier:
    """A class to classify images into music mood categories using CLIP model."""
    
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        """Initialize the classifier with a CLIP model.
        
        Args:
            model_name (str): Name of the CLIP model to use
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Enhanced activities/moods with descriptive adjectives for better matching
        self.activities = [
            # Study/Focus variations
            "serene classical music for focused studying",
            "calm instrumental music for deep concentration",
            "peaceful ambient music for productive work",
            "gentle piano music for academic focus",
            "soft background music for mental clarity",
            
            # Gaming variations
            "energetic electronic gaming music",
            "intense orchestral gaming soundtrack",
            "epic battle music for gaming",
            "dynamic electronic gaming beats",
            "powerful gaming adventure music",
            
            # Chill/Relax variations
            "soft relaxing lofi beats",
            "gentle ambient chill music",
            "peaceful nature sounds with music",
            "calming meditation soundtrack",
            "soothing acoustic relaxation",
            
            # Social variations
            "upbeat party music for socializing",
            "lively tropical house music",
            "fun pop music for gatherings",
            "vibrant dance music playlist",
            "cheerful social party mix",
            
            # Ambient variations
            "ethereal ambient soundscape",
            "dreamy atmospheric background",
            "floating ambient meditation music",
            "celestial space ambient sounds",
            "misty ambient drone music",
            
            # Reading variations
            "quiet classical music for reading",
            "soft instrumental reading music",
            "peaceful acoustic reading soundtrack",
            "gentle piano music for books",
            "calm ambient reading atmosphere"
        ]
        
        try:
            # Load model and processor only once during initialization
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.logger.info(f"Using device: {self.device}")
            
            self.model = CLIPModel.from_pretrained(model_name).to(self.device)
            self.processor = CLIPProcessor.from_pretrained(model_name)
            
            # Set model to evaluation mode
            self.model.eval()
            
        except Exception as e:
            self.logger.error(f"Error initializing model: {str(e)}")
            raise

    def preprocess_image(self, image_path: str) -> Optional[Image.Image]:
        """Preprocess the input image.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            PIL.Image: Processed image or None if processing fails
        """
        try:
            path = Path(image_path)
            if not path.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")
                
            image = Image.open(path).convert('RGB')
            return image
            
        except Exception as e:
            self.logger.error(f"Error preprocessing image: {str(e)}")
            return None

    def get_top_n_predictions(self, probs: torch.Tensor, n: int = 5) -> List[Tuple[str, float]]:
        """Get top N predictions with their confidence scores.
        
        Args:
            probs (torch.Tensor): Probability tensor
            n (int): Number of top predictions to return
            
        Returns:
            List[Tuple[str, float]]: List of (activity, confidence) pairs
        """
        top_probs, top_indices = torch.topk(probs, k=min(n, len(self.activities)))
        return [(self.activities[idx], prob.item() * 100) 
                for idx, prob in zip(top_indices[0], top_probs[0])]

    @torch.no_grad()
    def classify(self, image_path: str, top_n: int = 5) -> Optional[List[Tuple[str, float]]]:
        """Classify an image and return top N mood predictions with confidence scores.
        
        Args:
            image_path (str): Path to the image file
            top_n (int): Number of top predictions to return
            
        Returns:
            Optional[List[Tuple[str, float]]]: List of (mood, confidence) pairs or None if classification fails
        """
        try:
            image = self.preprocess_image(image_path)
            if image is None:
                return None
            
            inputs = self.processor(
                text=self.activities,
                images=image,
                return_tensors="pt",
                padding=True
            )
            
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            outputs = self.model(**inputs)
            probs = outputs.logits_per_image.softmax(dim=1)
            
            return self.get_top_n_predictions(probs, top_n)
            
        except Exception as e:
            self.logger.error(f"Error during classification: {str(e)}")
            return None

def main():
    """Main function to demonstrate the classifier usage."""
    classifier = ImageMoodClassifier()
    
    image_paths = [
        "../reading.jpg",
        "../learn.jpg",
        "../learn2.jpg"
    ]
    
    for image_path in image_paths:
        try:
            predictions = classifier.classify(image_path)
            
            if predictions:
                print(f"\nTop 5 music recommendations for {image_path}:")
                for mood, confidence in predictions:
                    print(f"- {mood}: {confidence:.2f}%")
            else:
                print(f"\nFailed to classify {image_path}")
                
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")

if __name__ == "__main__":
    main()
