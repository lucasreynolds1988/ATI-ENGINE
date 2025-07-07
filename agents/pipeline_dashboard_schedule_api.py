from fastapi import FastAPI, Header, HTTPException, Request
import os
import json

app = FastAPI()
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")
SCHEDULE_FILE = os.path.expanduser("~/Soap/agents/job_schedule.json")

def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/pipeline/schedule")
async def schedule_job(request: Request, x_api_token: str = Header(...)):
    get_token(x_api_token)
    data = await request.json()
    jobId = data.get("jobId")
    when = data.get("when")
    if not jobId or not when:
        raise HTTPException(status_code=400, detail="Missing jobId/when")
    jobs = []
    if os.path.isfile(SCHEDULE_FILE):
        with open(SCHEDULE_FILE) as f:
            jobs = json.load(f)
    jobs.append({"jobId": jobId, "when": when})
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(jobs, f)
    return {"status": "scheduled", "jobId": jobId, "when": when}
