import os
import json

def json_to_txt(json_file, txt_file):
    with open(json_file) as f:
        data = json.load(f)
    with open(txt_file, "w") as f:
        for k, v in data.items():
            f.write(f"{k}: {v}\n")
    print(f"Exported {json_file} to {txt_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        json_to_txt(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python pipeline_json_to_txt.py <input.json> <output.txt>")
