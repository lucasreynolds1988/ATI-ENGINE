#!/usr/bin/env python3
import time
import json

LOG_FILE = "/tmp/rotor_timing_log.json"

def log_event(engine, action, detail=""):
    t = time.time()
    event = {"engine": engine, "action": action, "detail": detail, "timestamp": t}
    try:
        with open(LOG_FILE, "r") as f:
            log = json.load(f)
    except Exception:
        log = []
    log.append(event)
    with open(LOG_FILE, "w") as f:
        json.dump(log, f)
    print(f"Rotor event logged: {event}")

def get_log():
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "get":
        print(json.dumps(get_log(), indent=2))
    else:
        log_event("openai", "vectorize", "Sample chunk for timing test")
