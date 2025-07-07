# ~/Soap/agents/agent_queue.py

import queue

AGENT_QUEUE = queue.Queue()

def add_agent_job(job):
    AGENT_QUEUE.put(job)

def get_next_agent_job():
    if AGENT_QUEUE.empty():
        return None
    return AGENT_QUEUE.get()
