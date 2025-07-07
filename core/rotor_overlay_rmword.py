import os

def rmword_overlay(filename, word):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    new_lines = [line for line in lines if word not in line]
    with open(path, "w") as f:
        f.writelines(new_lines)
    print(f"Removed all lines containing '{word}' from {filename}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        rmword_overlay(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python rotor_overlay_rmword.py <filename> <word>")
