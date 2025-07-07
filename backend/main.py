from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.responses import JSONResponse
# from fastapi.staticfiles import StaticFiles  # Comment out for dev, see below
import os

app = FastAPI()

# -------------------------------
# (OPTIONAL) Serve React static build (for production only)
# For development with React, comment out these two lines!
# frontend_dir = os.path.join(os.path.dirname(__file__), "static")
# app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")
# -------------------------------

@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI backend!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        pass

@app.get("/metrics")
def metrics():
    return {"status": "ok", "message": "Metrics endpoint is live!"}

@app.get("/log")
def log():
    return {"log": ["System started", "No errors detected"]}

@app.get("/pipeline/jobs")
def jobs():
    return {"jobs": [{"id": 1, "status": "running"}, {"id": 2, "status": "done"}]}

@app.post("/manuals/upload")
async def upload_manual(file: UploadFile = File(...)):
    contents = await file.read()
    out_path = f"/tmp/{file.filename}"
    with open(out_path, "wb") as f:
        f.write(contents)
    return JSONResponse(content={"filename": file.filename})
