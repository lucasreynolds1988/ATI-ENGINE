# ~/Soap/agents/arbiter_phase.py

import sys
import os
import json

def process(input_file):
    # Input: .mother.json; Output: .arbiter.json
    mother_file = f"{input_file}.mother.json"
    arbiter_file = f"{input_file}.arbiter.json"
    if not os.path.isfile(mother_file):
        print(f"Missing Mother output: {mother_file}")
        sys.exit(1)
    with open(mother_file, "r") as f:
        mother_data = json.load(f)
    # Example: Arbiter resolves conflicts
    arbiter_data = {
        "conflict": False,
        "arbiter_reviewed": True,
        "mother_data": mother_data
    }
    with open(arbiter_file, "w") as f:
        json.dump(arbiter_data, f, indent=2)
    print(f"Arbiter output written: {arbiter_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 arbiter_phase.py <input_file>")
        sys.exit(1)
    process(sys.argv[1])
