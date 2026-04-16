import os
import base64
from flask import Flask, jsonify, render_template_string, request
from google import genai

app = Flask(__name__)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

UI_FINGER = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #000; color: white; text-align: center; margin: 0; padding: 20px; }
        .camera-box { width: 250px; height: 250px; border-radius: 50%; border: 4px solid #38bdf8; overflow: hidden; margin: 20px auto; position: relative; }
        video { width: 100%; height: 100%; object-fit: cover; }
        .btn { background: #38bdf8; color: #000; padding: 20px; width: 100%; border: none; border-radius: 15px; font-weight: bold; font-size: 18px; }
        #res { margin-top: 20px; color: #38bdf8; font-weight: bold; }
    </style>
</head>
<body>
    <h2>🩺 VitalScan: Finger Scan</h2>
    <p style="font-size: 14px; color: #888;">Place your index finger over the camera</p>
    <div class="camera-box">
        <video id="webcam" autoplay playsinline></video>
    </div>
    <button class="btn" onclick="scanFinger()">ANALYZE BLOOD FLOW</button>
    <div id="res">Ready...</div>

    <script>
        const v = document.getElementById('webcam');
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } }).then(s => v.srcObject = s);

        function scanFinger() {
            const canvas = document.createElement('canvas');
            canvas.width = 300; canvas.height = 300;
            canvas.getContext('2d').drawImage(v, 0, 0, 300, 300);
            const data = canvas.toDataURL('image/jpeg', 0.5).split(',')[1];
            
            document.getElementById('res').innerText = "AI extracting pulse from pixels...";
            
            fetch('/api/finger_scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: data })
            })
            .then(r => r.json())
            .then(d => { document.getElementById('res').innerHTML = d.result; });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(UI_FINGER)

@app.route("/api/finger_scan", methods=["POST"])
def finger_scan():
    img_data = request.json['image']
    # Prompting Gemini to act as a Pulse Oximeter
    prompt = "This is a close-up image of a finger over a camera lens. Analyze the red/pink pixel density to estimate Heart Rate (BPM) and SpO2 (%)."
    
    resp = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[prompt, {'mime_type': 'image/jpeg', 'data': img_data}]
    )
    return jsonify({"result": resp.text})
