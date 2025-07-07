import os

def tail_log(filename="rotor_overlay.log", lines=20):
    logs_dir = os.path.expanduser("~/Soap/logs")
    fpath = os.path.join(logs_dir, filename)
    if not os.path.isfile(fpath):
        print(f"Log file {filename} not found.")
        return
    with open(fpath, "r") as f:
        content = f.readlines()
        for line in content[-lines:]:
            print(line.rstrip())

if __name__ == "__main__":
    tail_log()
