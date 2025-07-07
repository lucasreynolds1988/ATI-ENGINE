import os
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

@app.get("/health")
def health(x_api_token: str = Header(...)):
    get_token(x_api_token)
    if os.path.isfile(LOG):
        return {"status": "ok", "log_size": os.path.getsize(LOG)}
    else:
        return {"status": "log missing"}

# To run: uvicorn pipeline_dashboard_health:app --host 0.0.0.0 --port 5006
