import json
import os
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()
CONFIG = os.path.expanduser("~/Soap/agents/pipeline_config.json")
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")

def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.get("/roles")
def get_roles(x_api_token: str = Header(...)):
    get_token(x_api_token)
    with open(CONFIG) as f:
        cfg = json.load(f)
    return cfg.get("role_controls", {})

# To run: uvicorn pipeline_dashboard_roles:app --host 0.0.0.0 --port 5005
