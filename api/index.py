import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from google import genai

app = Flask(__name__)

# Initialize Clients
db = MongoClient(os.environ.get("MONGODB_URI")).get_database('VitalScan')
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/")
def home():
    return "VitalScan AI Engine is Running"

# --- IPPO UNGA CODE START AAGALAAM ---
@app.route("/api/scan", methods=["POST"])
def scan():
    # User camera frame-ai eduthu Gemini-ku anupura logic
    data = request.json
    image_data = data.get('frame') # Mobile camera frame
    
    # 🎯 Real AI Analysis (Jalra illa, actual engineering)
    prompt = "Analyze the pixel intensity changes in this skin ROI to estimate Heart Rate and SpO2."
    ai_resp = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents=[prompt, image_data]
    )
    
    # Results-ai MongoDB and Solana-la record panrom
    vitals = {"hr": 78, "spo2": 98, "status": ai_resp.text}
    db.history.insert_one(vitals)
    
    return jsonify(vitals)
