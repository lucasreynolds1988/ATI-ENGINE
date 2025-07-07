import json
import os

CONFIG = os.path.expanduser("~/Soap/agents/pipeline_config.json")
AGENTS_DIR = os.path.expanduser("~/Soap/agents")

def validate_config():
    with open(CONFIG) as f:
        cfg = json.load(f)
    missing = []
    for phase in cfg["phases"]:
        script_path = os.path.join(AGENTS_DIR, phase["script"])
        if not os.path.isfile(script_path):
            missing.append(phase["script"])
    if missing:
        print("Missing agent scripts in config:")
        for m in missing:
            print(" -", m)
    else:
        print("Config is valid, all agent scripts found.")

if __name__ == "__main__":
    validate_config()
