# ~/Soap/watchdog.py

import shutil

def get_free_home_space_mb():
    stat = shutil.disk_usage("/home")
    return stat.free / (1024 * 1024)  # MB

def disk_ok(threshold_mb=500):
    free_space = get_free_home_space_mb()
    print(f"📊 Free disk space: {free_space:.2f}MB")
    return free_space > threshold_mb

if __name__ == "__main__":
    if disk_ok():
        print("✅ Disk space is healthy.")
    else:
        print("❌ Warning: Low disk space!")
