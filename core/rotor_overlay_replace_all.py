import os

def replace_all_overlay(filename, old, new):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if os.path.isfile(path):
        with open(path, "r") as f:
            content = f.read()
        content = content.replace(old, new)
        with open(path, "w") as f:
            f.write(content)
        print(f"Replaced all occurrences of '{old}' with '{new}' in {filename}.")
    else:
        print(f"{filename} not found in overlay.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        replace_all_overlay(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python rotor_overlay_replace_all.py <filename> <old> <new>")
