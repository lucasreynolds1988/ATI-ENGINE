import os

def diff_lines_overlay(file1, file2):
    overlay = os.path.expanduser("~/Soap/overlay")
    f1 = os.path.join(overlay, file1)
    f2 = os.path.join(overlay, file2)
    if not os.path.isfile(f1) or not os.path.isfile(f2):
        print(f"Both files must exist in overlay: {file1}, {file2}")
        return
    with open(f1, "r") as a, open(f2, "r") as b:
        a_lines = set(a.readlines())
        b_lines = set(b.readlines())
    only_a = a_lines - b_lines
    only_b = b_lines - a_lines
    print(f"Lines only in {file1}:")
    for line in only_a:
        print(line.rstrip())
    print(f"Lines only in {file2}:")
    for line in only_b:
        print(line.rstrip())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        diff_lines_overlay(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python rotor_overlay_diff_lines.py <file1> <file2>")
