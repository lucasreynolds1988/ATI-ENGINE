# ATI Web App V3.2

## Overview
This is a full-stack web app for ATI V3.2 — your AI Technician Assistant.
- Backend: Python Flask with Gemini AI integration
- Frontend: React (Node.js)
- Node.js server serves frontend and proxies API to backend

## How to run

### Backend
```bash
cd ati-web-app/backend
pip install -r requirements.txt
export GEMINI_API_KEY="your_api_key_here"
python main.py

cat << 'EOF' > ati-web-app/backend/ingest.py
def ingest_manual(file_storage):
    if file_storage is None:
        raise ValueError("No manual file provided.")
    filename = file_storage.filename
    # For demo: save the manual to local folder (extend to vectorize, scan, etc.)
    save_path = f"./manuals/{filename}"
    import os
    os.makedirs("./manuals", exist_ok=True)
    file_storage.save(save_path)
    return f"Manual '{filename}' saved successfully."
