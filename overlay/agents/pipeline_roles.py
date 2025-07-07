import json
import os

CONFIG = os.path.expanduser("~/Soap/agents/pipeline_config.json")

def show_roles():
    with open(CONFIG) as f:
        cfg = json.load(f)
    roles = cfg.get("role_controls", {})
    print("Roles permitted to approve:", roles.get("approve_roles", []))
    print("Roles permitted to run:", roles.get("run_roles", []))

if __name__ == "__main__":
    show_roles()
