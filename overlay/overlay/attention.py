#!/usr/bin/env python3
import os

def main():
    home_dir = os.path.expanduser("~")
    trigger_path = os.path.join(home_dir, "Soap", ".trigger.rebuild")

    if not os.path.exists(trigger_path):
        print("⚠️ .trigger.rebuild not found. Creating it now...")
        with open(trigger_path, "w") as f:
            f.write("triggered")
        print("✅ .trigger.rebuild created.")
    else:
        print("✅ .trigger.rebuild already exists.")

    print("🧭 Attention check complete. System is awake.")

if __name__ == "__main__":
    main()
