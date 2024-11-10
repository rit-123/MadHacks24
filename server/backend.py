from flask import Flask, render_template, request, jsonify, flash, redirect
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import cv2
import base64
import numpy as np
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotifylogic import SpotifyActions
import pyautogui 
import random
from LLM import ImageMoodClassifier
from flask_cors import CORS
from PIL import Image
import io
from emotionanalysis2 import predict_emotion
app = Flask(__name__)
CORS(app)
# Connect Database
import mysql.connector

# Establish a connection
conn = mysql.connector.connect(
    host='localhost',
    user="root",
    password='madhacks2024',
    database='ListenTua',

)
db1 = conn.cursor()
llm = ImageMoodClassifier()
CLIENT_ID = '2486129522ca4ed8bf027362ebfd60b1'
CLIENT_SECRET = '76bd17dcb73548d49f7a45c22ab03c96'
REDIRECT_URI = 'http://localhost:5173/listen'

app.secret_key = 'your_secret_key_here'

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         redirect_uri=REDIRECT_URI,
                         scope="user-read-private user-library-read user-modify-playback-state user-read-playback-state user-read-email streaming")

spotifyObj = SpotifyActions()

@app.route("/register", methods=["POST"])
def register():
    body = request.get_json()
    if not body.get("username"):
        return jsonify({"message": "Username is required"}), 400
    elif not body.get("password"):
        return jsonify({"message": "Password is required"}), 400

    try:
        # Check if username exists
        db1.execute(f"SELECT * FROM users")
        rows = db1.fetchall()
        if any(row[0] == body.get("username") for row in rows):
            return jsonify({"message": "Username already exists"}), 409
        # Hash the password
        hashed_password = generate_password_hash(body.get("password"))
        # Insert the new user
        db1.execute(f"INSERT INTO users values (%s,%s)", (body.get("password"), hashed_password))
        conn.commit()

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

    return jsonify({"message": "Successfully registered"}), 200


@app.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    print(body.get("username"))
    # Ensure username was sumbitted
    if not body.get("username"):
        response = {
            "message": "Username is required"
        }
        return response, 400

    # Ensure password was submitted
    elif not body.get("password"):
        response = {
            "message": "password is required"
        }
        return response, 400

    # Query database for username
    db1.execute("SELECT * FROM users WHERE username = %s", [body.get("username")])
    # Ensure username exists and password is correct
    rows = db1.fetchall()
    for row in rows:
        if not row[0] or not check_password_hash(row[1], body.get("password")):
            response = {
                "message": "Invalid username or password"
            }
            return response, 403
    # Remember which user has logged in
    response ={
        "message" : "Successfully Logged In",
        "username" : body.get("username")
    }
    return response, 200


@app.route('/connect_spotify')
def index():
    auth_url = sp_oauth.get_authorize_url()
    return {"url":auth_url}, 200

@app.route('/callback')
def callback():
    print("hit callback")
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info['access_token']
    spotifyObj.setToken(access_token)
    return access_token #need to return another redirect URL here maybe?


@app.route('/screenshot', methods=["POST"])
def screenshot():
    try:
        data = request.get_json()
        base64_string = data['screenImageData'].split(',')[1]  # Remove data URL prefix
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))

        face64 = data['cameraImageData'].split(',')[1]
        fimdata = base64.b64decode(face64)
        im2 = Image.open(io.BytesIO(fimdata))
        thingy = predict_emotion(im2)
        mood, conf = llm.classify(image,thingy)[0]
        print("conf is ", conf)
        if conf<15:mood="lo fi beats"
        print(f"the mood is {mood}")
        search(mood)
        return {"status_code":200, "message":""}
    except Exception as e:
        print(e)
        return {"status_code":500, "message":"Server error"}
    
def search(mood):
    access_token = spotifyObj.access_token
    if not access_token:
        print("No access token")
        return jsonify({"error": "Access token missing or expired"}), 400
    query = mode = mood
    # query = body.get("query", "pop") #default to pop
    # mode = body.get("mode", "")
    print(access_token)
    songs = spotifyObj.getSongs(query=query, mode=mode)
    return jsonify(songs)

@app.route("/screen", methods=["POST"])
def submitScreen():
    requestBody = request.json()
    print(requestBody)

@app.route("/pause", methods = ["GET"])
def playSong():
    try:
        spotifyObj.pauseSong()
        return {"message": "pass"}, 200
    except Exception as e:
        print(e)
        return {"message":"some fail"}, 400
    

if __name__ == "__main__":
    app.run(debug=True)
