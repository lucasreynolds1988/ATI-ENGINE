import os

def rmempty_overlay():
    overlay = os.path.expanduser("~/Soap/overlay")
    count = 0
    for fname in os.listdir(overlay):
        fpath = os.path.join(overlay, fname)
        if os.path.isfile(fpath) and os.path.getsize(fpath) == 0:
            os.remove(fpath)
            print(f"Removed empty file: {fname}")
            count += 1
    print(f"Removed {count} empty files from overlay.")

if __name__ == "__main__":
    rmempty_overlay()
