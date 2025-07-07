import os

def keepuniq_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    if not os.path.isfile(path):
        print(f"{filename} not found in overlay.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    seen = set()
    uniq = []
    for line in lines:
        if line not in seen:
            uniq.append(line)
            seen.add(line)
    with open(path, "w") as f:
        f.writelines(uniq)
    print(f"Kept only unique lines in {filename}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        keepuniq_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_keepuniq.py <filename>")
