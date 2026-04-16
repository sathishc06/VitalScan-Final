import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from google import genai
from solana.rpc.api import Client

app = Flask(__name__)

# Vercel will pick these from your Environment Variables
db = MongoClient(os.environ.get("MONGODB_URI")).get_database('VitalScan')
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/")
def home():
    return "<h1>VitalScan AI Live</h1><p>Ready for MLH Prizes</p>"

@app.route("/api/scan", methods=["POST"])
def scan():
    vitals = {"hr": 74, "spo2": 99}
    db.history.insert_one(vitals)
    sol_status = Client("https://api.devnet.solana.com").is_connected()
    prompt = f"Analyze HR {vitals['hr']} and SpO2 {vitals['spo2']}."
    ai_resp = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
    return jsonify({"vitals": vitals, "ai_report": ai_resp.text, "solana": sol_status})
  
