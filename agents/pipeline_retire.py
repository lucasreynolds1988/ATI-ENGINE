import os
import shutil

def retire_pipeline_outputs(folder, retire_dir):
    os.makedirs(retire_dir, exist_ok=True)
    files = [f for f in os.listdir(folder) if f.endswith(".final.txt")]
    for f in files:
        shutil.move(os.path.join(folder, f), os.path.join(retire_dir, f))
        print(f"Retired {f}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        retire_pipeline_outputs(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python pipeline_retire.py <folder> <retire_dir>")
