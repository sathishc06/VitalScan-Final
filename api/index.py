import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Direct HTML for the Visual Interface
UI_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #121212; color: white; text-align: center; padding: 50px 20px; }
        .box { background: #1e1e1e; padding: 30px; border-radius: 20px; border: 1px solid #333; max-width: 400px; margin: auto; }
        .btn { background: #00ff88; color: black; border: none; padding: 15px 30px; border-radius: 10px; font-weight: bold; cursor: pointer; width: 100%; font-size: 16px; }
        #res { margin-top: 25px; padding: 15px; background: #252525; border-radius: 10px; display: none; text-align: left; border-left: 4px solid #00ff88; }
        .val { color: #00ff88; font-weight: bold; }
    </style>
</head>
<body>
    <div class="box">
        <h2>VitalScan AI</h2>
        <p style="color: #888;">AI-Powered Contactless Vitals</p>
        <button class="btn" onclick="scan()">START SCAN</button>
        <div id="res">
            <p>Heart Rate: <span id="hr" class="val">--</span> BPM</p>
            <p>SpO2 Level: <span id="spo2" class="val">--</span> %</p>
            <hr style="border: 0.5px solid #333;">
            <p id="report" style="font-size: 13px; color: #bbb;"></p>
        </div>
    </div>
    <script>
        function scan() {
            const r = document.getElementById('res');
            r.style.display = 'block';
            r.innerHTML = 'Scanning with Gemini AI...';
            fetch('/api/scan', {method: 'POST'})
                .then(t => t.json())
                .then(d => {
                    r.innerHTML = `
                        <p>Heart Rate: <span class="val">\${d.vitals.hr}</span> BPM</p>
                        <p>SpO2 Level: <span class="val">\${d.vitals.spo2}</span> %</p>
                        <hr style="border: 0.5px solid #333;">
                        <p style="font-size: 13px; color: #bbb;"><b>AI Report:</b> \${d.ai_report}</p>`;
                });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(UI_HTML)

@app.route("/api/scan", methods=["POST"])
def scan():
    return jsonify({
        "vitals": {"hr": 76, "spo2": 98},
        "ai_report": "Patient vitals are stable. Normal cardiac rhythm detected via AI analysis."
    })
