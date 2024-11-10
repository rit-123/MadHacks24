from flask import Flask, render_template, request, jsonify, flash, redirect
from werkzeug.security import check_password_hash, generate_password_hash
import base64
import numpy as np
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from flask_cors import CORS
from PIL import Image
import io
from emotionanalysis2 import predict_emotion
app = Flask(__name__)
CORS(app)


app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        # Get the image from the request
        face64 = data['cameraImageData'].split(',')[1]
        fimdata = base64.b64decode(face64)
        im2 = Image.open(io.BytesIO(fimdata))
        # Predict emotion
        prediction = predict_emotion(im2)
        return jsonify({"emotion": prediction[0], "confidence": prediction[1]})
    except Exception as e:
        return jsonify({"emotion": "happy"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)



