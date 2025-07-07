import os
import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)

EVENT_LOG = os.path.expanduser("~/Soap/logs/pipeline_event.log")

@sio.on("connect")
async def connect(sid, environ, auth):
    print(f"Socket connected: {sid}")

@sio.on("subscribe")
async def subscribe(sid, data):
    # When frontend subscribes, push all recent events
    if os.path.isfile(EVENT_LOG):
        with open(EVENT_LOG) as f:
            await sio.emit("eventlog", {"lines": f.readlines()}, room=sid)

def send_pipeline_event(event):
    sio.start_background_task(sio.emit, "eventlog", {"lines": [event]})

if __name__ == "__main__":
    uvicorn.run(sio_app, host="0.0.0.0", port=5007)
