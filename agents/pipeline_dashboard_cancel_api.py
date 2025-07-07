from fastapi import FastAPI, Header, HTTPException, Request
import os
import signal
import json

app = FastAPI()
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")
RUN_FILE = os.path.expanduser("~/Soap/agents/job_runs.json")

def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/pipeline/cancel")
async def cancel_job(request: Request, x_api_token: str = Header(...)):
    get_token(x_api_token)
    data = await request.json()
    jobId = data.get("jobId")
    if not jobId:
        raise HTTPException(status_code=400, detail="Missing jobId")
    # Look up the PID for this job
    if not os.path.isfile(RUN_FILE):
        raise HTTPException(status_code=404, detail="No running jobs recorded")
    with open(RUN_FILE) as f:
        runs = json.load(f)
    pid = runs.get(jobId)
    if not pid:
        raise HTTPException(status_code=404, detail="Job not running or already finished")
    try:
        os.kill(pid, signal.SIGTERM)  # For hard kill use signal.SIGKILL
        # Remove from job_runs.json after kill
        del runs[jobId]
        with open(RUN_FILE, "w") as f:
            json.dump(runs, f)
        return {"status": "cancelled", "jobId": jobId, "pid": pid}
    except Exception as e:
        return {"status": "error", "jobId": jobId, "error": str(e)}
