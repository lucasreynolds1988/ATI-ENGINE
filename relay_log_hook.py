# ~/Soap/relay_log_hook.py

import subprocess

def run_viewer(mode="summary"):
    """
    Modes:
      - "summary": Show summary report
      - "last": Show last 5 entries
      - "all": Show all entries
    """
    if mode == "summary":
        subprocess.run(["python3", "relay_log_viewer.py"], input="5\n0\n", text=True)
    elif mode == "last":
        subprocess.run(["python3", "relay_log_viewer.py"], input="3\n5\n0\n", text=True)
    elif mode == "all":
        subprocess.run(["python3", "relay_log_viewer.py"], input="1\n0\n", text=True)
    else:
        print(f"❌ Unknown mode: {mode}")

if __name__ == "__main__":
    run_viewer("summary")
