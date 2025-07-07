import os
import json
from core.rotor_overlay import log_event

def deny(input_file, admin_name, correction):
    json_file = f"{input_file}.arbiter.json"
    if not os.path.isfile(json_file):
        print(f"Missing arbiter file: {json_file}")
        return
    with open(json_file) as f:
        sop = json.load(f)
    sop["approved"] = False
    sop["denied_by"] = admin_name
    sop["admin_correction"] = correction
    out_file = f"{input_file}.denied.json"
    with open(out_file, "w") as f:
        json.dump(sop, f, indent=2)
    log_event(f"AdminDeny: {input_file} denied by {admin_name}")
    print(f"{input_file} denied by {admin_name} with correction.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        deny(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python pipeline_admin_deny.py <input_file> <admin_name> <correction>")
