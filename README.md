# MoodMelody - Where AI Meets Music! 🎵

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.0%2B-61dafb)](https://reactjs.org/)

MoodMelody is an innovative AI-powered music companion that automatically adapts your music to your current activity and emotional state. Using advanced computer vision and machine learning, it creates the perfect soundtrack for every moment of your day.

## ✨ Features

- **Real-time Activity Detection**: Analyzes your current task through periodic screenshots
- **Emotion Recognition**: Captures your mood through facial expression analysis
- **Smart Music Selection**: Automatically curates and plays music that matches your context
- **Seamless Spotify Integration**: Direct integration with your Spotify account
- **Privacy-First Design**: Secure handling of all personal data
- **Cross-Platform Support**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

1. Clone the repository:
git clone https://github.com/yourusername/moodmelody.git
cd moodmelody

2. Install dependencies:
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install

3. Set up environment variables:
cp .env.example .env
# Add your Spotify API credentials

4.Run the application:
# Backend
python app.py

# Frontend
npm run dev


## 🛠️ Technology Stack

- **Frontend**: React.js, TailwindCSS, shadcn/ui
- **Backend**: Flask, Python
- **AI/ML**: 
  - CLIP model for activity detection
  - OpenCV for emotion recognition
  - Custom feature selection algorithms
- **Database**: SQLite/MySQL
- **APIs**: Spotify Web API

## 📊 How It Works

1. **Activity Detection**
   - Takes screenshots every 15-20 seconds
   - Processes images through CLIP model
   - Classifies current activity (coding, reading, gaming, etc.)

2. **Emotion Analysis**
   - Captures facial expressions via webcam
   - Analyzes emotional state using OpenCV
   - Determines current mood

3. **Music Selection**
   - Combines activity and emotion data
   - Applies feature selection algorithms
   - Queries Spotify API for matching music
   - Automatically adjusts playback

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 🎯 Example Usage
# Example of our feature selection process
from sklearn.feature_selection import SelectKBest, f_classif

def select_music_features(X, y, k=10):
    selector = SelectKBest(score_func=f_classif, k=k)
    X_new = selector.fit_transform(X, y)
    return X_new, selector


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- CLIP model by OpenAI
- Spotify Web API
- scikit-learn community
- All our contributors and supporters

## 🌟 Project Highlights

### Inspiration
As students and developers, we've all experienced the struggle of maintaining focus while managing our music during work sessions. The constant need to switch playlists or find the right music that matches our current task and mood often breaks our concentration. This inspired us to create MoodMelody - a smart music companion that automatically adapts to both your activity and emotional state.

### Challenges We Overcame
- Optimizing real-time processing of screenshots and facial analysis
- Fine-tuning the CLIP model for accurate activity detection
- Developing robust algorithms for context-aware music selection
- Implementing secure data handling for user privacy
- Seamless integration of multiple AI models with Spotify API

### Future Roadmap
- Personalized music learning based on user preferences
- Support for multiple music streaming platforms
- More sophisticated activity detection algorithms
- Collaborative features for shared workspaces
- Expanded emotion detection capabilities
- Integration with productivity tracking tools

---

**Note**: This project was created with the goal of enhancing productivity and creating perfect musical atmospheres for every moment of your day. We're constantly working to improve it and welcome your feedback!

For detailed API documentation and advanced usage, please visit our [Wiki](wiki).

*Made with ❤️ by the MoodMelody Team*
