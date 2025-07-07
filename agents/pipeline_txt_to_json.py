import os
import json

def txt_to_json(txt_file, json_file):
    data = {}
    with open(txt_file) as f:
        for line in f:
            if ": " in line:
                k, v = line.rstrip("\n").split(": ", 1)
                data[k] = v
    with open(json_file, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Exported {txt_file} to {json_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        txt_to_json(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python pipeline_txt_to_json.py <input.txt> <output.json>")
