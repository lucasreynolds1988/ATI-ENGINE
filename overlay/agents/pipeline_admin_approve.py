import os
import json
from core.rotor_overlay import log_event

def approve(input_file, admin_name):
    json_file = f"{input_file}.arbiter.json"
    if not os.path.isfile(json_file):
        print(f"Missing arbiter file: {json_file}")
        return
    with open(json_file) as f:
        sop = json.load(f)
    sop["approved"] = True
    sop["approved_by"] = admin_name
    out_file = f"{input_file}.approved.json"
    with open(out_file, "w") as f:
        json.dump(sop, f, indent=2)
    log_event(f"AdminApproval: {input_file} approved by {admin_name}")
    print(f"{input_file} approved by {admin_name}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        approve(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python pipeline_admin_approve.py <input_file> <admin_name>")
