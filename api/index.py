import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from google import genai

app = Flask(__name__)

# Config - Vercel will pick these from your Environment Variables
db = MongoClient(os.environ.get("MONGODB_URI")).get_database('VitalScan')
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/")
def home():
    return "<h1>VitalScan AI Live</h1><p>Ready for MLH Prizes</p>"

@app.route("/api/scan", methods=["POST"])
def scan():
    # Simulation logic for hackathon submission
    vitals = {"heart_rate": 78, "spo2": 98}
    db.history.insert_one(vitals)
    
    prompt = f"Analyze HR {vitals['heart_rate']} and SpO2 {vitals['spo2']}."
    ai_report = client.models.generate_content(model="gemini-1.5-flash", contents=prompt).text
    
    return jsonify({"vitals": vitals, "ai_report": ai_report})
