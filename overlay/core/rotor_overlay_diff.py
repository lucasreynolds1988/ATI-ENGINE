import os
import filecmp

def overlay_diff(other_dir):
    overlay = os.path.expanduser("~/Soap/overlay")
    dcmp = filecmp.dircmp(overlay, other_dir)
    print("Files only in overlay:", dcmp.left_only)
    print("Files only in other_dir:", dcmp.right_only)
    print("Files differing:", dcmp.diff_files)
    print("Common files:", dcmp.common_files)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        overlay_diff(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_diff.py <other_dir>")
