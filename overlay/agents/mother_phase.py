# ~/Soap/agents/mother_phase.py

import sys
import os
import json

def process(input_file):
    # Input: .father.json; Output: .mother.json
    father_file = f"{input_file}.father.json"
    mother_file = f"{input_file}.mother.json"
    if not os.path.isfile(father_file):
        print(f"Missing Father output: {father_file}")
        sys.exit(1)
    with open(father_file, "r") as f:
        father_data = json.load(f)
    # Example: Add safety checks, modify as needed
    mother_data = {
        "safety_reviewed": True,
        "father_data": father_data
    }
    with open(mother_file, "w") as f:
        json.dump(mother_data, f, indent=2)
    print(f"Mother output written: {mother_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 mother_phase.py <input_file>")
        sys.exit(1)
    process(sys.argv[1])
