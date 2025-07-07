import os
import json

CONFIG = os.path.expanduser("~/Soap/agents/pipeline_config.json")

def load_config():
    with open(CONFIG) as f:
        cfg = json.load(f)
    print(json.dumps(cfg, indent=2))

if __name__ == "__main__":
    load_config()
