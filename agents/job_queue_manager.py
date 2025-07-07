# ~/Soap/agents/job_queue_manager.py

import os
import json

QUEUE_FILE = os.path.expanduser("~/Soap/logs/job_queue.json")

def enqueue_job(job):
    queue = []
    if os.path.isfile(QUEUE_FILE):
        with open(QUEUE_FILE, "r") as f:
            queue = json.load(f)
    queue.append(job)
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f)

def dequeue_job():
    if not os.path.isfile(QUEUE_FILE):
        return None
    with open(QUEUE_FILE, "r") as f:
        queue = json.load(f)
    if not queue:
        return None
    job = queue.pop(0)
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f)
    return job
