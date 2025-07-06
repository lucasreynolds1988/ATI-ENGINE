# ~/Soap/app.py

import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from backend.routes.synthesize_route import generate_sop_from_manuals

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# File type checker
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home screen
@app.route('/')
def index():
    return render_template("index.html")

# SOP preview generator route
@app.route('/generate', methods=['POST'])
def generate_preview_sop():
    project_description = request.form.get("purpose")
    files = request.files.getlist("manuals")

    if not project_description or not files:
        return jsonify({"error": "Missing purpose or files"}), 400

    manuals = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            print(f"✔ Saved: {filepath}")  # Debug log
            manuals.append(filepath)

    # Generate SOP
    sop = generate_sop_from_manuals(project_description, manuals)

    # Clean up
    for f in manuals:
        if os.path.exists(f):
            os.remove(f)

    return jsonify(sop)

# Launch Flask app
if __name__ == '__main__':
    print("🔥 Flask server is starting...")
    app.run(debug=True, host='0.0.0.0', port=5000)
