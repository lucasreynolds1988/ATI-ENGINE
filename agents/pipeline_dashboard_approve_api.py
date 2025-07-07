from fastapi import FastAPI, Header, HTTPException, Request
import os
import json

app = FastAPI()
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")

def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/pipeline/approve")
async def approve_job(request: Request, x_api_token: str = Header(...)):
    get_token(x_api_token)
    data = await request.json()
    jobId = data.get("jobId")
    arbiter_file = f"{jobId}.arbiter.json"
    if not os.path.isfile(arbiter_file):
        raise HTTPException(status_code=404, detail="Arbiter file not found")
    with open(arbiter_file) as f:
        sop = json.load(f)
    sop["approved"] = True
    sop["approved_by"] = "API"
    approved_file = f"{jobId}.approved.json"
    with open(approved_file, "w") as f:
        json.dump(sop, f, indent=2)
    return {"status": "approved"}
