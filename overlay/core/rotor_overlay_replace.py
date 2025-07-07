import os

def replace_line_overlay(filename, lineno, text):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    if 0 <= lineno < len(lines):
        lines[lineno] = text + "\n"
        with open(path, "w") as f:
            f.writelines(lines)
        print(f"Replaced line {lineno} in {filename}")
    else:
        print(f"Invalid line number {lineno}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        replace_line_overlay(sys.argv[1], int(sys.argv[2]), " ".join(sys.argv[3:]))
    else:
        print("Usage: python rotor_overlay_replace.py <filename> <lineno> <text>")
