# ~/Soap/governor.py

import shutil

def get_free_home_space_mb():
    stat = shutil.disk_usage("/home")
    return stat.free / (1024 * 1024)  # in MB

def get_rpm():
    free_space = get_free_home_space_mb()
    print(f"📊 Free disk: {free_space:.2f}MB")

    if free_space > 1500:
        return 2.0  # Fast
    elif 800 < free_space <= 1500:
        return 3.0  # Normal
    elif 500 < free_space <= 800:
        return 4.0  # Slow
    else:
        return None  # Signal watchdog override

if __name__ == "__main__":
    rpm = get_rpm()
    if rpm:
        print(f"✅ Rotor RPM set to {rpm} seconds")
    else:
        print("❌ RPM override triggered — not enough space to operate")
