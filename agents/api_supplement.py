# ~/Soap/agents/api_supplement.py

from fastapi import APIRouter, File, UploadFile, Header, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
import os
import json
from pipeline_dashboard_api import get_token

router = APIRouter()

DATA_DIR = os.path.expanduser("~/Soap/data/")
MANUALS_DIR = os.path.expanduser("~/Soap/manuals/")
SOPS_DIR = os.path.expanduser("~/Soap/sops/")
TRAINING_DIR = os.path.expanduser("~/Soap/training/")
LOGS_DIR = os.path.expanduser("~/Soap/logs/")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MANUALS_DIR, exist_ok=True)
os.makedirs(SOPS_DIR, exist_ok=True)
os.makedirs(TRAINING_DIR, exist_ok=True)

# --------- 1. MANUALS ---------

@router.post("/manuals/upload")
async def upload_manual(x_api_token: str = Header(...), file: UploadFile = File(...)):
    get_token(x_api_token)
    dest = os.path.join(MANUALS_DIR, file.filename)
    with open(dest, "wb") as f:
        f.write(await file.read())
    # Optionally, log upload
    histfile = os.path.join(LOGS_DIR, "upload_history.json")
    hist = []
    if os.path.isfile(histfile):
        with open(histfile) as hf:
            try: hist = json.load(hf)
            except: hist = []
    hist.append({"filename": file.filename, "user": "system", "date": ""})
    with open(histfile, "w") as hf:
        json.dump(hist, hf)
    return {"filename": file.filename}

@router.get("/manuals/list")
def manuals_list(x_api_token: str = Header(...)):
    get_token(x_api_token)
    files = os.listdir(MANUALS_DIR)
    return {"files": files}

@router.get("/manuals/upload-history")
def manuals_upload_history(x_api_token: str = Header(...)):
    get_token(x_api_token)
    histfile = os.path.join(LOGS_DIR, "upload_history.json")
    if os.path.isfile(histfile):
        with open(histfile) as f:
            try: hist = json.load(f)
            except: hist = []
    else:
        hist = []
    return {"history": hist}

@router.delete("/manuals/delete/{filename}")
def manuals_delete(filename: str, x_api_token: str = Header(...)):
    get_token(x_api_token)
    fpath = os.path.join(MANUALS_DIR, filename)
    if os.path.isfile(fpath):
        os.remove(fpath)
        return {"deleted": filename}
    return JSONResponse({"error": "Not found"}, status_code=404)

# --------- 2. SOPS ---------

@router.get("/sops/list")
def sops_list(x_api_token: str = Header(...)):
    get_token(x_api_token)
    files = os.listdir(SOPS_DIR)
    return {"files": files}

@router.post("/sops/approve/{filename}")
def sops_approve(filename: str, x_api_token: str = Header(...)):
    get_token(x_api_token)
    # Mark file as approved (here, just a status file)
    status_file = os.path.join(SOPS_DIR, f"{filename}.approved")
    with open(status_file, "w") as f:
        f.write("approved")
    return {"status": f"{filename} approved"}

@router.get("/sops/download/{filename}")
def sops_download(filename: str, x_api_token: str = Header(...)):
    get_token(x_api_token)
    fpath = os.path.join(SOPS_DIR, filename)
    if os.path.isfile(fpath):
        return FileResponse(fpath, filename=filename)
    return JSONResponse({"error": "Not found"}, status_code=404)

@router.get("/final/{fileId}")
def sop_final(fileId: str, x_api_token: str = Header(...)):
    get_token(x_api_token)
    final_path = os.path.join(SOPS_DIR, f"{fileId}.final.txt")
    if os.path.isfile(final_path):
        with open(final_path) as f:
            content = f.read()
        return {"content": content}
    return JSONResponse({"error": "Not found"}, status_code=404)

# --------- 3. SCAVENGER ---------

@router.post("/scavenger/start")
def scavenger_start(x_api_token: str = Header(...), url: str = Form(...)):
    get_token(x_api_token)
    # Normally, you'd launch a job. Here just echo.
    histfile = os.path.join(LOGS_DIR, "scavenger_history.json")
    hist = []
    if os.path.isfile(histfile):
        with open(histfile) as hf:
            try: hist = json.load(hf)
            except: hist = []
    hist.append({"url": url, "date": "", "status": "started"})
    with open(histfile, "w") as hf:
        json.dump(hist, hf)
    return {"status": f"scavenger started for {url}"}

@router.get("/scavenger/history")
def scavenger_history(x_api_token: str = Header(...)):
    get_token(x_api_token)
    histfile = os.path.join(LOGS_DIR, "scavenger_history.json")
    if os.path.isfile(histfile):
        with open(histfile) as f:
            try: hist = json.load(f)
            except: hist = []
    else:
        hist = []
    return {"history": hist}

# --------- 4. AGENTS ---------

@router.get("/agents/list")
def agents_list(x_api_token: str = Header(...)):
    get_token(x_api_token)
    # List agents by filename for now
    agents = [
        "watson_phase.py", "father_phase.py", "mother_phase.py",
        "arbiter_phase.py", "soap_phase.py"
    ]
    return {"agents": agents}

@router.get("/agents/status")
def agents_status(x_api_token: str = Header(...)):
    get_token(x_api_token)
    # Fake status map
    status = {
        "watson": "OK",
        "father": "OK",
        "mother": "OK",
        "arbiter": "OK",
        "soap": "OK"
    }
    return {"statuses": status}

@router.post("/agents/config/{agent}")
def agents_config(agent: str, x_api_token: str = Header(...), config: str = Form(...)):
    get_token(x_api_token)
    cfgfile = os.path.join(DATA_DIR, f"{agent}.cfg")
    with open(cfgfile, "w") as f:
        f.write(config)
    return {"status": f"{agent} config updated"}

# --------- 5. TECHNICIANS ---------

@router.get("/technicians/list")
def technicians_list(x_api_token: str = Header(...)):
    get_token(x_api_token)
    # Demo techs
    techs = [
        {"id": 1, "name": "Lucas Reynolds", "role": "Admin"},
        {"id": 2, "name": "Tech User", "role": "Technician"}
    ]
    return {"technicians": techs}

@router.get("/technicians/me")
def technicians_me(x_api_token: str = Header(...)):
    get_token(x_api_token)
    # Fake self-profile
    profile = {
        "name": "Lucas Reynolds",
        "role": "Admin",
        "email": "lucasreynolds1988@gmail.com",
        "joined": "2023-01-01"
    }
    return {"profile": profile}

# --------- 6. TRAINING ---------

@router.post("/training/upload")
async def training_upload(x_api_token: str = Header(...), file: UploadFile = File(...)):
    get_token(x_api_token)
    dest = os.path.join(TRAINING_DIR, file.filename)
    with open(dest, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}

@router.get("/training/list")
def training_list(x_api_token: str = Header(...)):
    get_token(x_api_token)
    files = os.listdir(TRAINING_DIR)
    return {"resources": files}
