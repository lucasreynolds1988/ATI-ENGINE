import os
import time
import re

def smart_cleanup(pattern=None, max_age_days=None, min_size=None):
    overlay = os.path.expanduser("~/Soap/overlay")
    now = time.time()
    deleted = 0
    for fname in os.listdir(overlay):
        fpath = os.path.join(overlay, fname)
        stat = os.stat(fpath)
        remove = False
        if pattern and not re.search(pattern, fname):
            continue
        if max_age_days and (now - stat.st_mtime) > (max_age_days * 86400):
            remove = True
        if min_size and os.path.getsize(fpath) < min_size:
            remove = True
        if remove:
            os.remove(fpath)
            print(f"Deleted: {fname}")
            deleted += 1
    print(f"Smart cleanup complete. Deleted {deleted} files.")

if __name__ == "__main__":
    import sys
    # Usage: python rotor_overlay_cleanup_smart.py <pattern> <max_age_days> <min_size_bytes>
    args = sys.argv[1:]
    pattern = args[0] if len(args) > 0 and args[0] != "None" else None
    max_age_days = int(args[1]) if len(args) > 1 and args[1] != "None" else None
    min_size = int(args[2]) if len(args) > 2 and args[2] != "None" else None
    smart_cleanup(pattern, max_age_days, min_size)
