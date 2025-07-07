import os
import time

def stat_overlay():
    overlay = os.path.expanduser("~/Soap/overlay")
    print("File\t\tSize\t\tLast Modified")
    for fname in os.listdir(overlay):
        fpath = os.path.join(overlay, fname)
        if os.path.isfile(fpath):
            sz = os.path.getsize(fpath)
            mtime = time.ctime(os.path.getmtime(fpath))
            print(f"{fname}\t{sz} bytes\t{mtime}")

if __name__ == "__main__":
    stat_overlay()
