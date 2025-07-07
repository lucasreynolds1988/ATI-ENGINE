import os

def insert_overlay(filename, lineno, text):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    idx = max(0, min(int(lineno), len(lines)))
    lines.insert(idx, text + "\n")
    with open(path, "w") as f:
        f.writelines(lines)
    print(f"Inserted line in {filename} at {lineno}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        insert_overlay(sys.argv[1], int(sys.argv[2]), " ".join(sys.argv[3:]))
    else:
        print("Usage: python rotor_overlay_insert.py <filename> <lineno> <text>")
