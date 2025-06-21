# ~/Soap/status_check.py

import os
import shutil

def check_disk_usage(path='/home'):
    total, used, free = shutil.disk_usage(path)
    print(f"📁 Path         : {path}")
    print(f"💾 Total        : {total // (2**30)} GB")
    print(f"📊 Used         : {used // (2**30)} GB")
    print(f"📉 Free         : {free // (2**30)} GB")
    print(f"🔺 Percent Used : {used / total:.1%}")

def main():
    print("🛑 +CODE-RED+ SYSTEM CHECK INITIATED")
    check_disk_usage()
    print("✅ Status check complete.")

if __name__ == "__main__":
    main()
