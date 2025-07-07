from fastapi import FastAPI, Header, HTTPException, Query
import os

app = FastAPI()
HISTORY_FILE = os.path.expanduser("~/Soap/logs/pipeline_history.log")
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")

def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.get("/pipeline/history")
def get_history(x_api_token: str = Header(...), search: str = Query(default=None)):
    get_token(x_api_token)
    if not os.path.isfile(HISTORY_FILE):
        return {"lines": []}
    with open(HISTORY_FILE) as f:
        lines = f.readlines()
    if search:
        lines = [l for l in lines if search.lower() in l.lower()]
    return {"lines": lines}
