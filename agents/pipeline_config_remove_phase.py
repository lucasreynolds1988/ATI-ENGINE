import os
import json

CONFIG = os.path.expanduser("~/Soap/agents/pipeline_config.json")

def remove_phase(name):
    with open(CONFIG) as f:
        cfg = json.load(f)
    cfg["phases"] = [ph for ph in cfg["phases"] if ph["name"] != name]
    with open(CONFIG, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"Removed phase {name} from config.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        remove_phase(sys.argv[1])
    else:
        print("Usage: python pipeline_config_remove_phase.py <phase_name>")
