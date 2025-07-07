import os
import time

def log_history(input_file, status):
    log_file = os.path.expanduser("~/Soap/logs/pipeline_history.log")
    with open(log_file, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {input_file} | {status}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        log_history(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python pipeline_history_log.py <input_file> <status>")
