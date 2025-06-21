# ~/Soap/space_drive.py

import os
import shutil
from pathlib import Path

def format_size(bytes):
    for unit in ['B','KB','MB','GB','TB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} PB"

def get_disk_usage(path):
    usage = shutil.disk_usage(path)
    return {
        "Path": path,
        "Total": format_size(usage.total),
        "Used": format_size(usage.used),
        "Free": format_size(usage.free),
        "Percent Used": f"{(usage.used / usage.total) * 100:.1f}%"
    }

def count_files_and_size(base_dir):
    total_size = 0
    file_count = 0
    for dirpath, _, filenames in os.walk(base_dir):
        for f in filenames:
            try:
                fp = Path(os.path.join(dirpath, f))
                if fp.is_file():
                    total_size += fp.stat().st_size
                    file_count += 1
            except:
                continue
    return file_count, format_size(total_size)

def main():
    print("🛰️ +SPACE-DRIVE+ STATUS CHECK\n")

    for path in ["/home", "/root"]:
        print(f"📁 Scanning: {path}")
        usage = get_disk_usage(path)
        for k, v in usage.items():
            print(f"   {k:<14}: {v}")
        
        count, size = count_files_and_size(path)
        print(f"   Files Found   : {count}")
        print(f"   Total Size    : {size}")
        print("")

    print("✅ SPACE-DRIVE REPORT COMPLETE")

if __name__ == "__main__":
    main()
