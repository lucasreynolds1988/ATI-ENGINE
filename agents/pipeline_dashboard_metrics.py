import os
import time
import json
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()
LOG = os.path.expanduser("~/Soap/logs/rotor_overlay.log")
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")

def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.get("/metrics")
def get_metrics(x_api_token: str = Header(...)):
    get_token(x_api_token)
    stats = {"pipelines": 0, "failures": 0}
    if os.path.isfile(LOG):
        with open(LOG) as f:
            for line in f:
                if "Pipeline: Complete" in line or "DynamicPipeline:" in line:
                    stats["pipelines"] += 1
                if "Pipeline failed" in line or "FAILED" in line:
                    stats["failures"] += 1
    stats["uptime"] = int(time.time() - os.stat(LOG).st_ctime) if os.path.isfile(LOG) else 0
    return stats

# To run: uvicorn pipeline_dashboard_metrics:app --host 0.0.0.0 --port 5004
