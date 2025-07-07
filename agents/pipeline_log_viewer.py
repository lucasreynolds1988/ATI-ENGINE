import os

def view_logs():
    log_file = os.path.expanduser("~/Soap/logs/rotor_overlay.log")
    if not os.path.isfile(log_file):
        print("No log file found.")
        return
    with open(log_file, "r") as f:
        for line in f:
            print(line.rstrip())

if __name__ == "__main__":
    view_logs()
