from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
import os
from pipeline_dashboard_pdf_export import export_pdf

app = FastAPI()
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")

def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.get("/jobpdf/{jobId}")
def jobpdf(jobId: str, x_api_token: str = Header(...)):
    get_token(x_api_token)
    outfile = f"{jobId}.report.pdf"
    export_pdf(jobId, outfile)
    if not os.path.isfile(outfile):
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(outfile)
