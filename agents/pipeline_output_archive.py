import os
import shutil

def archive_outputs(folder, archive_dir):
    os.makedirs(archive_dir, exist_ok=True)
    files = [f for f in os.listdir(folder) if f.endswith(".final.txt")]
    for f in files:
        shutil.move(os.path.join(folder, f), os.path.join(archive_dir, f))
        print(f"Archived {f}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        archive_outputs(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python pipeline_output_archive.py <folder> <archive_dir>")
