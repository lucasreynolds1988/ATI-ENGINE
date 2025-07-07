# ~/Soap/agents/pipeline_dashboard_api.py

from fastapi import FastAPI, HTTPException, Header, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import os
import json
import subprocess

app = FastAPI()

# Paths
CONFIG = os.path.expanduser("~/Soap/agents/pipeline_config.json")
LOG = os.path.expanduser("~/Soap/logs/rotor_overlay.log")
PIPELINE_HISTORY = os.path.expanduser("~/Soap/logs/pipeline_history.log")
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")

# Token Check
def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

# Config endpoint
@app.get("/config")
def get_config(x_api_token: str = Header(...)):
    get_token(x_api_token)
    with open(CONFIG) as f:
        return json.load(f)

# Log endpoint
@app.get("/log")
def get_log(x_api_token: str = Header(...)):
    get_token(x_api_token)
    if os.path.isfile(LOG):
        return FileResponse(LOG)
    else:
        return JSONResponse({"error": "Log file missing."}, status_code=404)

# Pipeline history endpoint
@app.get("/pipeline/history")
def get_pipeline_history(x_api_token: str = Header(...)):
    get_token(x_api_token)
    if os.path.isfile(PIPELINE_HISTORY):
        with open(PIPELINE_HISTORY) as f:
            return {"lines": f.readlines()}
    return JSONResponse({"error": "History log missing."}, status_code=404)

# Pipeline status endpoint
@app.get("/pipeline/status/{input_file}")
def get_pipeline_status(input_file: str, x_api_token: str = Header(...)):
    get_token(x_api_token)
    status = {}
    exts = [".watson.json", ".father.json", ".mother.json", ".arbiter.json", ".final.txt"]
    for ext in exts:
        fname = f"{input_file}{ext}"
        status[ext] = os.path.isfile(fname)
    return status

# Run pipeline
@app.post("/pipeline/run/{input_file}")
def run_pipeline(input_file: str, x_api_token: str = Header(...)):
    get_token(x_api_token)
    subprocess.Popen([
        "python3",
        os.path.expanduser("~/Soap/agents/pipeline_dynamic_runner.py"),
        input_file
    ])
    return {"status": "Pipeline started", "input_file": input_file}

# Roles endpoint
@app.get("/roles")
def get_roles(x_api_token: str = Header(...)):
    get_token(x_api_token)
    return {
        "roles": [
            "Admin",
            "Technician",
            "Curator",
            "Guest"
        ]
    }

# Metrics endpoint
@app.get("/metrics")
def get_metrics(x_api_token: str = Header(...)):
    get_token(x_api_token)
    metrics = {
        "system_status": "OK",
        "jobs_running": count_running_jobs(),
        "last_job_time": get_last_job_time(),
        "rotor_status": get_rotor_status()
    }
    return metrics

# Pipeline jobs endpoint
@app.get("/pipeline/jobs")
def get_pipeline_jobs(x_api_token: str = Header(...)):
    get_token(x_api_token)
    jobs = read_job_status_list()
    return {"jobs": jobs}

# ---- Utility functions ----
def count_running_jobs():
    job_log = os.path.expanduser("~/Soap/logs/pipeline_jobs.log")
    count = 0
    if os.path.isfile(job_log):
        with open(job_log) as f:
            for line in f:
                if '"status": "running"' in line:
                    count += 1
    return count

def get_last_job_time():
    job_log = os.path.expanduser("~/Soap/logs/pipeline_jobs.log")
    last_time = None
    if os.path.isfile(job_log):
        with open(job_log) as f:
            lines = f.readlines()
            for line in reversed(lines):
                try:
                    entry = json.loads(line)
                    if "timestamp" in entry:
                        last_time = entry["timestamp"]
                        break
                except Exception:
                    continue
    return last_time

def get_rotor_status():
    rotor_status_file = os.path.expanduser("~/Soap/logs/rotor_status.log")
    if os.path.isfile(rotor_status_file):
        with open(rotor_status_file) as f:
            status = f.read().strip()
            return status
    return "unknown"

def read_job_status_list():
    job_log = os.path.expanduser("~/Soap/logs/pipeline_jobs.log")
    jobs = []
    if os.path.isfile(job_log):
        with open(job_log) as f:
            for line in f:
                try:
                    job = json.loads(line)
                    if all(k in job for k in ("id", "status", "type", "timestamp")):
                        jobs.append(job)
                except Exception:
                    continue
    return jobs

# --- Mount API supplement endpoints ---
from api_supplement import router as supplement_router
app.include_router(supplement_router)

# To run:
# uvicorn pipeline_dashboard_api:app --host 0.0.0.0 --port 5003
