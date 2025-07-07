import os

def merge_overlay(prefix, outfilename):
    overlay = os.path.expanduser("~/Soap/overlay")
    files = sorted([f for f in os.listdir(overlay) if f.startswith(prefix) and ".part" in f])
    if not files:
        print(f"No files with prefix {prefix} found in overlay.")
        return
    with open(os.path.join(overlay, outfilename), "w") as out:
        for fname in files:
            with open(os.path.join(overlay, fname), "r") as part:
                out.writelines(part.readlines())
    print(f"Merged into {outfilename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        merge_overlay(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python rotor_overlay_merge.py <prefix> <outfilename>")
