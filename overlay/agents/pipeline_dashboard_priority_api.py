from fastapi import FastAPI, Header, HTTPException, Request
import os
import json

app = FastAPI()
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")
PRIORITY_FILE = os.path.expanduser("~/Soap/agents/job_priority.json")

def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/pipeline/priority")
async def set_priority(request: Request, x_api_token: str = Header(...)):
    get_token(x_api_token)
    data = await request.json()
    jobId = data.get("jobId")
    priority = data.get("priority")
    if not jobId or not priority:
        raise HTTPException(status_code=400, detail="Missing jobId/priority")
    priorities = {}
    if os.path.isfile(PRIORITY_FILE):
        with open(PRIORITY_FILE) as f:
            priorities = json.load(f)
    priorities[jobId] = priority
    with open(PRIORITY_FILE, "w") as f:
        json.dump(priorities, f)
    return {"status": "priority_set", "jobId": jobId, "priority": priority}
