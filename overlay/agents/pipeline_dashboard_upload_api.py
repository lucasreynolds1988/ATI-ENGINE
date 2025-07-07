from fastapi import FastAPI, File, UploadFile, Header, HTTPException
import os
import shutil

app = FastAPI()
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")
UPLOAD_DIR = os.path.expanduser("~/Soap/agents/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/upload")
async def upload_job(file: UploadFile = File(...), x_api_token: str = Header(...)):
    get_token(x_api_token)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"status": "uploaded", "filename": file.filename}
