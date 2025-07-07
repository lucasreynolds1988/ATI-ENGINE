# ~/Soap/agents/agent_utils.py

import os

def safe_file_write(path, data, mode="w"):
    with open(path, mode) as f:
        f.write(data)
