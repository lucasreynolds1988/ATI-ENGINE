from fastapi import FastAPI, Header, HTTPException, Request
import os
import subprocess

app = FastAPI()
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")

def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/pipeline/retry")
async def retry_job(request: Request, x_api_token: str = Header(...)):
    get_token(x_api_token)
    data = await request.json()
    jobId = data.get("jobId")
    if not jobId:
        raise HTTPException(status_code=400, detail="Missing jobId")
    subprocess.Popen([
        "python3",
        os.path.expanduser("~/Soap/agents/pipeline_dynamic_runner.py"),
        jobId
    ])
    return {"status": "retry_triggered", "jobId": jobId}
