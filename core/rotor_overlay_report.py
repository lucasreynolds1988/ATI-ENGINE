import os
import time

def overlay_report():
    overlay = os.path.expanduser("~/Soap/overlay")
    report = []
    for fname in os.listdir(overlay):
        path = os.path.join(overlay, fname)
        sz = os.path.getsize(path)
        mtime = time.ctime(os.path.getmtime(path))
        report.append((fname, sz, mtime))
    report.sort(key=lambda x: x[0])
    print("Overlay File Report:")
    for fname, sz, mtime in report:
        print(f"{fname}\t{sz} bytes\t{mtime}")
    print(f"Total files: {len(report)}")

if __name__ == "__main__":
    overlay_report()
