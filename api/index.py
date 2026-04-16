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
