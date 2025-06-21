# ~/Soap/relay_log_viewer.py

import json
from pathlib import Path
from datetime import datetime

LOG_PATH = Path.home() / "Soap/data/relay_log.json"

def load_log():
    if not LOG_PATH.exists():
        print("⚠️ No relay log found.")
        return []
    with open(LOG_PATH, "r") as f:
        return json.load(f)

def print_entry(entry, index):
    ts = datetime.fromisoformat(entry["timestamp"])
    print(f"\n🔹 Entry #{index}")
    print(f"🕒 Time   : {ts.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🧬 SHA    : {entry['sha'][:12]}...")
    print(f"📦 Size   : {entry['size']} bytes")
    print(f"🎯 Target : {entry['target']}")
    print(f"🔖 Chunk  : {entry['chunk_id']}")

def filter_by_target(entries, target):
    return [e for e in entries if e["target"].lower() == target.lower()]

def tail(entries, count=5):
    return entries[-count:] if len(entries) >= count else entries

def menu():
    print("\n📋 Relay Log Viewer Options:")
    print("  1. View ALL")
    print("  2. Filter by TARGET (MongoDB, GCS, GitHub)")
    print("  3. View LAST N entries")
    print("  0. Exit")

def main():
    entries = load_log()
    if not entries:
        print("🚫 No entries to show.")
        return

    while True:
        menu()
        choice = input("\nSelect an option: ").strip()
        
        if choice == "1":
            for idx, entry in enumerate(entries):
                print_entry(entry, idx)

        elif choice == "2":
            target = input("Enter target (MongoDB/GCS/GitHub): ").strip()
            filtered = filter_by_target(entries, target)
            if not filtered:
                print(f"⚠️ No entries for target: {target}")
            else:
                for idx, entry in enumerate(filtered):
                    print_entry(entry, idx)

        elif choice == "3":
            try:
                n = int(input("How many entries (default 5): ") or "5")
                for idx, entry in enumerate(tail(entries, n)):
                    print_entry(entry, idx)
            except ValueError:
                print("⚠️ Invalid number")

        elif choice == "0":
            print("👋 Exiting viewer.")
            break

        else:
            print("❌ Invalid selection.")

if __name__ == "__main__":
    main()
