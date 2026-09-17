import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename
from model import predict_disease

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# DB connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="krushi"
)

# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (data['username'], data['password']))
    user = cursor.fetchone()

    if user:
        return jsonify({"status": "success", "user": user})
    return jsonify({"status": "fail"}), 401

# ================= MILK =================
@app.route("/milk", methods=["POST"])
def add_milk():
    data = request.json
    cursor = db.cursor()

    query = "INSERT INTO milk (animal, litre) VALUES (%s, %s)"
    cursor.execute(query, (data['animal'], data['litre']))
    db.commit()

    return jsonify({"message": "Milk data saved"})

# ================= CROP =================
@app.route("/crop", methods=["POST"])
def crop():
    data = request.json
    soil = data['soil'].lower()
    season = data['season'].lower()

    # Smart logic
    if soil == "black" and season == "summer":
        result = "Cotton"
    elif season == "winter":
        result = "Wheat"
    else:
        result = "Rice"

    return jsonify({"crop": result})

# ================= AI DETECTION =================
@app.route("/detect", methods=["POST"])
def detect():
    if "image" not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files["image"]
    filename = secure_filename(file.filename)

    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    disease, confidence, health = predict_disease(path)

    # Suggestion logic
    if disease == "Leaf Spot":
        solution = "Use fungicide spray"
    elif disease == "Blight":
        solution = "Remove infected leaves"
    else:
        solution = "Plant is healthy"

    return jsonify({
        "disease": disease,
        "confidence": confidence,
        "health": health,
        "solution": solution
    })

# ================= RUN =================
if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)