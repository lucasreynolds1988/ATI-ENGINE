import os
import time

EVENT_LOG = os.path.expanduser("~/Soap/logs/pipeline_event.log")

def add_event(event):
    with open(EVENT_LOG, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {event}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        add_event(" ".join(sys.argv[1:]))
    else:
        print("Usage: python pipeline_dashboard_add_event.py <event_text>")
