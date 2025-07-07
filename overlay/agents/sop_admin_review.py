# ~/Soap/agents/sop_admin_review.py

import sys
import os
import json

def review(input_file):
    # Review .final.txt for admin approval
    final_file = f"{input_file}.final.txt"
    if not os.path.isfile(final_file):
        print(f"Missing final SOP: {final_file}")
        sys.exit(1)
    with open(final_file, "r") as f:
        content = f.read()
    # Example admin review output (could mark as approved, rejected, etc.)
    print("Admin Review of Final SOP:")
    print(content)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 sop_admin_review.py <input_file>")
        sys.exit(1)
    review(sys.argv[1])
