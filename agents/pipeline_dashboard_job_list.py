from fastapi import FastAPI, Header, HTTPException
import os
import glob

app = FastAPI()
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")

def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.get("/pipeline/jobs")
def list_jobs(x_api_token: str = Header(...)):
    get_token(x_api_token)
    jobs = [os.path.splitext(os.path.basename(f))[0] for f in glob.glob("*.json") if ".watson" not in f and ".father" not in f and ".mother" not in f and ".arbiter" not in f]
    return {"jobs": jobs}
