# ~/Soap/web_overlay.py

from flask import Flask, jsonify, render_template, request
import os
import subprocess
import shutil

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("overlay.html")

@app.route("/status")
def status():
    df = shutil.disk_usage("/home")
    usage = {
        "total": round(df.total / (1024 ** 3), 2),
        "used": round(df.used / (1024 ** 3), 2),
        "free": round(df.free / (1024 ** 3), 2)
    }
    return jsonify({
        "disk": usage,
        "rotor": "Running",
        "channels": ["GitHub ✅", "MongoDB ✅", "GCS ✅"]
    })

@app.route("/trigger", methods=["POST"])
def trigger_rotor():
    subprocess.Popen(["python3", "rotor_fusion.py"])
    return jsonify({"status": "Triggered +CODE-RED+"})

@app.route("/restore", methods=["POST"])
def restore_fusion():
    subprocess.Popen(["python3", "fusion_loader.py"])
    return jsonify({"status": "Started fusion restore"})

@app.route("/shutdown", methods=["POST"])
def shutdown_system():
    targets = ["rotor_core.py", "rotor_fusion.py", "fusion_loader.py"]
    for name in targets:
        subprocess.call(f"pkill -f {name}", shell=True)
    return jsonify({"status": "SPIN-DOWN complete: All systems terminated."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
