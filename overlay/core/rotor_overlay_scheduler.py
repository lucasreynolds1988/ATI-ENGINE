import subprocess
import time

def run_on_interval(script, interval_seconds):
    print(f"Running {script} every {interval_seconds} seconds. Ctrl+C to stop.")
    while True:
        subprocess.run(["python3", script])
        time.sleep(interval_seconds)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        run_on_interval(sys.argv[1], int(sys.argv[2]))
    else:
        print("Usage: python rotor_overlay_scheduler.py <script> <interval_seconds>")
