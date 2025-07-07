import os
import time
import socketio

sio = socketio.Client()
sio.connect("http://localhost:5007")

def emit_pipeline_event(event):
    sio.emit("eventlog", {"lines": [event]})

def emit_event(event):
    emit_pipeline_event(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {event}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        emit_event(" ".join(sys.argv[1:]))
    else:
        print("Usage: python pipeline_dashboard_event_emit.py <event_text>")
