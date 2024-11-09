from flask import Flask, render_template, request, jsonify, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import cv2
import base64
import numpy as np

app = Flask(__name__)

# Connect Database
import mysql.connector

# Establish a connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='madhacks2024',
    database='ListenTua'
)
db1 = conn.cursor()

# Execute a query
cursor.execute("SELECT * FROM mytable")

# Fetch all rows
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close the connection
conn.close()

@app.route("/register", methods=["POST"])
def register():
    # Ensure username was submitted
    if not request.form.get("username"):
        response = {
            "message": "Username is required"
        }
        return response, 400

    # Ensure password was submitted
    elif not request.form.get("password"):
        response = {
            "message": "Password is required"
        }
        return response, 400


    # Query database for username
    db1.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])
    rows = db1.fetchall()
    for row in rows:
        # Make sure username is unique
        if row[0] == request.form.get("username"):
            response = {
                "message": "Username already exists"
            }
            return response, 403

    # Hash password
    hashedPassword = generate_password_hash(request.form.get("password"))

    # Insert username and hashed password into database
    db1.execute("INSERT INTO users (username, hash) VALUES(?, ?)", [request.form.get("username"), hashedPassword])
    conn.commit()

    response = {
        "message": "Successfully registered"
    }
    return response, 200


@app.route("/login", methods=["POST"])
def login():

    # Ensure username was sumbitted
    if not request.form.get("username"):
        response = {
            "message": "Username is required"
        }
        return response, 400

    # Ensure password was submitted
    elif not request.form.get("password"):
        response = {
            "message": "password is required"
        }
        return response, 400

    # Query database for username
    db1.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])
    # Ensure username exists and password is correct
    rows = db1.fetchall()
    for row in rows:
        if not row[0] or not check_password_hash(row[1], request.form.get("password")):
             response = {
                "message": "Invalid username or password"
            }
        return response, 403
    # Remember which user has logged in
    response ={
        "message" : "Successfully Logged In",
        "username" : request.form.get("username")
    }
    return response, 200

@app.route("/screen", methods=["POST"])
def submitScreen():
    requestBody = request.json()
    print(requestBody)

    

if __name__=="__main__":
    app.run(debug=True)