import os
import base64
from flask import Flask, jsonify, render_template_string, request
from google import genai

app = Flask(__name__)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# ACTUAL Camera Interface
UI_LIVE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #000; color: white; text-align: center; margin: 0; }
        video { width: 100%; max-width: 400px; border-radius: 20px; border: 2px solid #38bdf8; }
        .btn { background: #38bdf8; color: #000; padding: 20px; width: 80%; border: none; border-radius: 15px; font-weight: bold; margin-top: 20px; cursor: pointer; }
        #log { margin-top: 20px; font-size: 14px; color: #38bdf8; }
    </style>
</head>
<body>
    <h1>🩺 VitalScan Live</h1>
    <video id="webcam" autoplay playsinline></video>
    <br>
    <button class="btn" onclick="captureAndScan()">SCAN MY FACE</button>
    <div id="log">Ready to Scan...</div>

    <script>
        const video = document.getElementById('webcam');
        navigator.mediaDevices.getUserMedia({ video: true }).then(stream => video.srcObject = stream);

        function captureAndScan() {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            const frame = canvas.toDataURL('image/jpeg').split(',')[1];
            
            document.getElementById('log').innerHTML = "AI Analyzing pixels...";
            
            fetch('/api/live_scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: frame })
            })
            .then(r => r.json())
            .then(d => {
                document.getElementById('log').innerHTML = "<b>Result:</b> " + d.analysis;
            });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(UI_LIVE)

@app.route("/api/live_scan", methods=["POST"])
def live_scan():
    data = request.json['image']
    # Sending ACTUAL frame to Gemini Vision
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[
            "Analyze this face frame for vascular fluctuations. Estimate Heart Rate and SpO2 based on skin pixel intensity.",
            {'mime_type': 'image/jpeg', 'data': data}
        ]
    )
    return jsonify({"analysis": response.text})
