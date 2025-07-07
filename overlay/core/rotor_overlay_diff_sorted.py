import os

def diff_sorted_overlay(file1, file2):
    overlay = os.path.expanduser("~/Soap/overlay")
    f1 = os.path.join(overlay, file1)
    f2 = os.path.join(overlay, file2)
    if not os.path.isfile(f1) or not os.path.isfile(f2):
        print(f"Both files must exist in overlay: {file1}, {file2}")
        return
    with open(f1, "r") as a, open(f2, "r") as b:
        a_lines = sorted(set(a.readlines()))
        b_lines = sorted(set(b.readlines()))
    print("--- Only in", file1, "---")
    for line in set(a_lines) - set(b_lines):
        print(line.rstrip())
    print("--- Only in", file2, "---")
    for line in set(b_lines) - set(a_lines):
        print(line.rstrip())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        diff_sorted_overlay(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python rotor_overlay_diff_sorted.py <file1> <file2>")
