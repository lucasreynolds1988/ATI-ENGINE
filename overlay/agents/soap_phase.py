# ~/Soap/agents/soap_phase.py

import sys
import os
import json

def process(input_file):
    # Input: .arbiter.json; Output: .final.txt
    arbiter_file = f"{input_file}.arbiter.json"
    final_file = f"{input_file}.final.txt"
    if not os.path.isfile(arbiter_file):
        print(f"Missing Arbiter output: {arbiter_file}")
        sys.exit(1)
    with open(arbiter_file, "r") as f:
        arbiter_data = json.load(f)
    # Example: Final synthesis/explanation
    with open(final_file, "w") as f:
        f.write("Final SOP Output\n")
        f.write(json.dumps(arbiter_data, indent=2))
    print(f"Soap output written: {final_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 soap_phase.py <input_file>")
        sys.exit(1)
    process(sys.argv[1])
