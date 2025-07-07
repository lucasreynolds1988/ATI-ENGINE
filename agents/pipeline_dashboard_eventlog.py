import os
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()
EVENT_LOG = os.path.expanduser("~/Soap/logs/pipeline_event.log")
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")

def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.get("/events")
def get_events(x_api_token: str = Header(...)):
    get_token(x_api_token)
    if os.path.isfile(EVENT_LOG):
        with open(EVENT_LOG) as f:
            return {"lines": f.readlines()}
    else:
        return {"error": "Event log missing"}

# To run: uvicorn pipeline_dashboard_eventlog:app --host 0.0.0.0 --port 5007
