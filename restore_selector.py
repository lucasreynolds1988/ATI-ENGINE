# ~/Soap/restore_selector.py

import json
from pathlib import Path
from datetime import datetime
import subprocess

LOG_PATH = Path.home() / "Soap/data/relay_log.json"
RESTORE_SCRIPT = Path.home() / "Soap/fusion_restore_v2.py"

def load_log():
    if not LOG_PATH.exists():
        print("❌ No relay log found.")
        return []
    try:
        with open(LOG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error reading log: {e}")
        return []

def display_entries(log):
    print("\n📊 Available Restore Points:\n")
    for i, entry in enumerate(log):
        try:
            ts = datetime.fromisoformat(entry["timestamp"])
            sha = entry.get("sha", "?")[:12]
            cloud = entry.get("cloud", "?")
            print(f"  {i:>2} | {cloud:<7} | {ts.strftime('%Y-%m-%d %H:%M:%S')} | {sha}")
        except Exception as e:
            print(f"⚠️  Skipping corrupted entry #{i}: {e}")

def get_selection(max_index):
    while True:
        try:
            selection = int(input(f"\nSelect index to rebuild (0–{max_index}): "))
            if 0 <= selection <= max_index:
                return selection
            print("❌ Invalid index.")
        except ValueError:
            print("❌ Please enter a valid number.")

def restore_by_sha(log, index):
    entry = log[index]
    sha = entry.get("sha")
    cloud = entry.get("cloud")
    if not sha or not cloud:
        print("❌ Invalid entry format.")
        return
    print(f"\n🔁 Rebuilding from: {cloud} [{sha[:12]}]")
    try:
        subprocess.run(["python3", str(RESTORE_SCRIPT), sha], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Restore script failed: {e}")

def main():
    log = load_log()
    if not log:
        return
    display_entries(log)
    selection = get_selection(len(log) - 1)
    restore_by_sha(log, selection)

if __name__ == "__main__":
    main()
