import os
import time
import subprocess

def watch_and_trigger(folder):
    files_seen = set(os.listdir(folder))
    print(f"Watching {folder} for new .json files...")
    while True:
        current = set(os.listdir(folder))
        new_files = current - files_seen
        for f in new_files:
            if f.endswith(".json"):
                print(f"Triggering pipeline for {f}")
                subprocess.Popen([
                    "python3",
                    os.path.expanduser("~/Soap/agents/pipeline_supervisor.py"),
                    os.path.join(folder, f)
                ])
        files_seen = current
        time.sleep(5)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        watch_and_trigger(sys.argv[1])
    else:
        print("Usage: python pipeline_filewatch_trigger.py <folder>")
