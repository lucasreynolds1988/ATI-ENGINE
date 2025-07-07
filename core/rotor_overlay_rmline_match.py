import os

def rmline_match_overlay(filename, match):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    kept = [line for line in lines if match not in line]
    with open(path, "w") as f:
        f.writelines(kept)
    print(f"Removed lines containing '{match}' from {filename}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        rmline_match_overlay(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python rotor_overlay_rmline_match.py <filename> <match>")
