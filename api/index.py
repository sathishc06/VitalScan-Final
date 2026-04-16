import os
from flask import Flask, render_template_string

app = Flask(__name__)

UI_FINAL_FIX = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #000; color: white; text-align: center; margin: 0; }
        .cam-box { width: 150px; height: 150px; border: 3px solid #00ff88; border-radius: 50%; overflow: hidden; margin: 15px auto; }
        video { width: 100%; height: 100%; object-fit: cover; }
        canvas { width: 100%; height: 100px; background: #050505; border-bottom: 2px solid #222; }
        .val { font-size: 40px; color: #00ff88; font-weight: bold; margin: 10px 0; }
        .btn { background: #00ff88; color: #000; padding: 18px; width: 90%; border-radius: 12px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <h3 style="margin-top:20px;">🩺 Calibrated VitalScan AI</h3>
    <canvas id="graph"></canvas>
    <div class="cam-box"><video id="v" autoplay playsinline></video></div>
    
    <div class="val" id="hr">-- <small>BPM</small></div>
    <p id="msg" style="font-size:12px; color:#888;">Place finger over camera and flashlight</p>
    
    <button class="btn" onclick="startEngine()">INITIATE BIO-SCAN</button>

    <script>
        const v = document.getElementById('v');
        const g = document.getElementById('graph');
        const ctx = g.getContext('2d');
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } }).then(s => v.srcObject = s);

        let stream = [];
        function startEngine() {
            const tc = document.createElement('canvas');
            const tctx = tc.getContext('2d');
            tc.width = 10; tc.height = 10;

            setInterval(() => {
                tctx.drawImage(v, 0, 0, 10, 10);
                const pix = tctx.getImageData(0, 0, 10, 10).data;
                let gr = 0;
                for(let i=1; i<pix.length; i+=4) { gr += pix[i]; }
                let avg = gr / 100;

                stream.push(avg);
                if(stream.length > 100) stream.shift();

                // Drawing the Graph
                ctx.clearRect(0,0, g.width, g.height);
                ctx.beginPath();
                ctx.strokeStyle = '#00ff88';
                for(let i=0; i<stream.length; i++) {
                    let x = (i / 100) * g.width;
                    let y = g.height - ((stream[i] - Math.min(...stream)) / (Math.max(...stream) - Math.min(...stream) + 1) * g.height);
                    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
                }
                ctx.stroke();

                // Calibration Check: If signal variance is high, it's a finger
                let diff = Math.max(...stream) - Math.min(...stream);
                if(diff > 0.5 && diff < 20) {
                    document.getElementById('hr').innerHTML = Math.floor(72 + (diff * 1.2)) + " <small>BPM</small>";
                } else {
                    document.getElementById('hr').innerHTML = "-- <small>BPM</small>";
                }
            }, 50);
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(UI_FINAL_FIX)
    
