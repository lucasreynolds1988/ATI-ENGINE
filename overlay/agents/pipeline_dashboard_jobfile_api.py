from fastapi import FastAPI, Header, HTTPException
import os

app = FastAPI()
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")

def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.get("/jobfile/{jobId}")
def get_jobfile(jobId: str, x_api_token: str = Header(...)):
    get_token(x_api_token)
    filename = f"{jobId}.arbiter.json"
    if not os.path.isfile(filename):
        return {"contents": "(Job file not found)"}
    with open(filename) as f:
        return {"contents": f.read()}
