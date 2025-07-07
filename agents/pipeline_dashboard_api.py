from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.responses import FileResponse, JSONResponse
import os
import json

app = FastAPI()
CONFIG = os.path.expanduser("~/Soap/agents/pipeline_config.json")
LOG = os.path.expanduser("~/Soap/logs/rotor_overlay.log")
PIPELINE_HISTORY = os.path.expanduser("~/Soap/logs/pipeline_history.log")
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")

def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.get("/config")
def get_config(x_api_token: str = Header(...)):
    get_token(x_api_token)
    with open(CONFIG) as f:
        return json.load(f)

@app.get("/log")
def get_log(x_api_token: str = Header(...)):
    get_token(x_api_token)
    if os.path.isfile(LOG):
        return FileResponse(LOG)
    else:
        return JSONResponse({"error": "Log file missing."}, status_code=404)

@app.get("/pipeline/history")
def get_pipeline_history(x_api_token: str = Header(...)):
    get_token(x_api_token)
    if os.path.isfile(PIPELINE_HISTORY):
        with open(PIPELINE_HISTORY) as f:
            return {"lines": f.readlines()}
    return JSONResponse({"error": "History log missing."}, status_code=404)

@app.get("/pipeline/status/{input_file}")
def get_pipeline_status(input_file: str, x_api_token: str = Header(...)):
    get_token(x_api_token)
    status = {}
    exts = [".watson.json", ".father.json", ".mother.json", ".arbiter.json", ".final.txt"]
    for ext in exts:
        fname = f"{input_file}{ext}"
        status[ext] = os.path.isfile(fname)
    return status

@app.post("/pipeline/run/{input_file}")
def run_pipeline(input_file: str, x_api_token: str = Header(...)):
    get_token(x_api_token)
    import subprocess
    subprocess.Popen([
        "python3",
        os.path.expanduser("~/Soap/agents/pipeline_dynamic_runner.py"),
        input_file
    ])
    return {"status": "Pipeline started", "input_file": input_file}

# To run: uvicorn pipeline_dashboard_api:app --host 0.0.0.0 --port 5003
