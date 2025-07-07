import os
import time

def auto_clean(folder, interval=600):
    print(f"Starting auto-clean every {interval}s in {folder}. Ctrl+C to stop.")
    while True:
        for f in os.listdir(folder):
            if any(f.endswith(ext) for ext in [".watson.json", ".father.json", ".mother.json", ".arbiter.json", ".final.txt"]):
                path = os.path.join(folder, f)
                age = time.time() - os.path.getmtime(path)
                if age > interval:
                    os.remove(path)
                    print(f"Auto-removed {f}")
        time.sleep(interval)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 600
        auto_clean(sys.argv[1], interval)
    else:
        print("Usage: python pipeline_auto_clean.py <folder> [interval_seconds]")
