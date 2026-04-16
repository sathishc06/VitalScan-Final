import os
from flask import Flask, jsonify, render_template_string, request
from google import genai

app = Flask(__name__)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

UI_FIXED = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #000; color: white; text-align: center; padding: 20px; }
        .circle { width: 180px; height: 180px; border-radius: 50%; border: 4px solid #00ff88; overflow: hidden; margin: 20px auto; }
        video { width: 100%; height: 100%; object-fit: cover; }
        .btn { background: #00ff88; color: #000; padding: 18px; width: 100%; border: none; border-radius: 12px; font-weight: bold; font-size: 16px; }
        #res { margin-top: 25px; font-size: 20px; color: #00ff88; }
    </style>
</head>
<body>
    <h3>🩺 VitalScan: Finger Mode</h3>
    <p style="font-size: 13px; color: #aaa;">Place finger FIRMLY on camera lens</p>
    <div class="circle"><video id="v" autoplay playsinline></video></div>
    <button class="btn" onclick="quickScan()">FAST SCAN (3s)</button>
    <div id="res">Waiting for finger...</div>

    <script>
        const v = document.getElementById('v');
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } }).then(s => v.srcObject = s);

        function quickScan() {
            const c = document.createElement('canvas');
            c.width = 100; c.height = 100; // Super small for speed
            c.getContext('2d').drawImage(v, 0, 0, 100, 100);
            const data = c.toDataURL('image/jpeg', 0.3).split(',')[1];
            
            document.getElementById('res').innerText = "AI Processing...";
            
            fetch('/api/fast_scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ img: data })
            })
            .then(r => r.json())
            .then(d => { document.getElementById('res').innerHTML = d.val; });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(UI_FIXED)

@app.route("/api/fast_scan", methods=["POST"])
def fast_scan():
    img = request.json['img']
    # Professional prompt for fast extraction
    prompt = "Clinical extraction: Heart Rate (BPM) and SpO2 from this finger pulse frame. Short response only."
    resp = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[prompt, {'mime_type': 'image/jpeg', 'data': img}]
    )
    return jsonify({"val": resp.text})
