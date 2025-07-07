import os
import json

CONFIG = os.path.expanduser("~/Soap/agents/pipeline_config.json")

def add_phase(name, script):
    with open(CONFIG) as f:
        cfg = json.load(f)
    cfg["phases"].append({"name": name, "script": script})
    with open(CONFIG, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"Added phase {name} ({script}) to config.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        add_phase(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python pipeline_config_add_phase.py <phase_name> <script>")
