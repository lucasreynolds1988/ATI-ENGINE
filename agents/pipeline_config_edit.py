import os
import json

CONFIG = os.path.expanduser("~/Soap/agents/pipeline_config.json")

def edit_delay(new_delay):
    with open(CONFIG) as f:
        cfg = json.load(f)
    cfg["delay_seconds"] = new_delay
    with open(CONFIG, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"Updated delay_seconds to {new_delay} in config.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        edit_delay(int(sys.argv[1]))
    else:
        print("Usage: python pipeline_config_edit.py <new_delay_seconds>")
