import os

def linecount_match_overlay(filename, match):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    count = sum(1 for line in lines if match in line)
    print(f"{filename}: {count} lines match '{match}'.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        linecount_match_overlay(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python rotor_overlay_linecount_match.py <filename> <match>")
