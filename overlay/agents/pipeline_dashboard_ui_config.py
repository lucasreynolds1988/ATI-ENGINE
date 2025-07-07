import os
import json

CONFIG = os.path.expanduser("~/Soap/agents/pipeline_config.json")

def export_for_ui(outfile="pipeline_ui_config.json"):
    with open(CONFIG) as f:
        cfg = json.load(f)
    # Add any UI-specific customizations here as needed
    with open(outfile, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"Exported pipeline config for UI: {outfile}")

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "pipeline_ui_config.json"
    export_for_ui(out)
