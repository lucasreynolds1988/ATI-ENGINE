# ~/Soap/agents/job_status_tracker.py

import os
import json

def log_job_status(job_id, status, job_type, timestamp):
    log_path = os.path.expanduser("~/Soap/logs/pipeline_jobs.log")
    entry = {
        "id": job_id,
        "status": status,
        "type": job_type,
        "timestamp": timestamp
    }
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")
