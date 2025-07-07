import os
import time
import json

CLUSTER_FILE = os.path.expanduser("~/Soap/agents/cluster_nodes.json")
HEARTBEAT_FILE = os.path.expanduser("~/Soap/agents/cluster_heartbeat.json")

def send_heartbeat(host):
    now = time.time()
    beats = {}
    if os.path.isfile(HEARTBEAT_FILE):
        with open(HEARTBEAT_FILE) as f:
            beats = json.load(f)
    beats[host] = now
    with open(HEARTBEAT_FILE, "w") as f:
        json.dump(beats, f)
    print(f"Heartbeat sent for {host} at {now}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        send_heartbeat(sys.argv[1])
    else:
        print("Usage: python pipeline_dashboard_node_heartbeat.py <host>")
