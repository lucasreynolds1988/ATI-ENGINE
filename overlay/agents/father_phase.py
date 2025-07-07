# ~/Soap/agents/father_phase.py

import sys
import os
import json

def process(input_file):
    # Input: .watson.json; Output: .father.json
    watson_file = f"{input_file}.watson.json"
    father_file = f"{input_file}.father.json"
    if not os.path.isfile(watson_file):
        print(f"Missing Watson output: {watson_file}")
        sys.exit(1)
    with open(watson_file, "r") as f:
        watson_data = json.load(f)
    # Example: Validate or enrich Watson data
    father_data = {
        "logic_pass": True,
        "watson_data": watson_data
    }
    with open(father_file, "w") as f:
        json.dump(father_data, f, indent=2)
    print(f"Father output written: {father_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 father_phase.py <input_file>")
        sys.exit(1)
    process(sys.argv[1])
