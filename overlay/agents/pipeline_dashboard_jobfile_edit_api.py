from fastapi import FastAPI, Header, HTTPException, Request
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

@app.post("/jobfile/{jobId}")
async def edit_jobfile(jobId: str, request: Request, x_api_token: str = Header(...)):
    get_token(x_api_token)
    data = await request.json()
    filename = f"{jobId}.arbiter.json"
    with open(filename, "w") as f:
        f.write(data.get("contents", ""))
    return {"status": "saved"}
