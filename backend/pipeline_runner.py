import os
import subprocess

def run_pipeline_job(file_id: str):
    log = f"Running pipeline for file: {file_id}"
    try:
        result = subprocess.run(["python3", "agents/watson_phase.py", file_id], capture_output=True, text=True)
        log += "\n" + result.stdout
    except Exception as e:
        log += f"\nError: {str(e)}"
    return log
