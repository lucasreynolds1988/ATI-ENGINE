# ~/Soap/rotor_timing_chain.py

import time
import json
import os
from datetime import datetime

TIMING_INTERVALS = {
    "MongoDB": 4,
    "GCS": 6,
    "GitHub": 8
}
LOG_FILE = os.path.expanduser("~/Soap/logs/relay_log.json")
TIMING_FILE = os.path.expanduser("~/Soap/logs/timing_chain.json")

print("⏱️ Rotor Timing Chain Active...")

if not os.path.exists(LOG_FILE):
    print("❌ relay_log.json not found.")
    exit(1)

with open(LOG_FILE, 'r') as f:
    entries = json.load(f)

last_pulse = {target: 0 for target in TIMING_INTERVALS}
violations = []

for entry in entries:
    cloud = entry.get("cloud")
    ts = entry.get("timestamp")
    try:
        current_time = datetime.fromisoformat(ts).timestamp()
    except:
        continue

    if cloud in last_pulse:
        delta = current_time - last_pulse[cloud]
        interval = TIMING_INTERVALS[cloud]
        if last_pulse[cloud] > 0 and delta < interval:
            violations.append({
                "cloud": cloud,
                "timestamp": ts,
                "delta": round(delta, 2),
                "required": interval
            })
        last_pulse[cloud] = current_time

with open(TIMING_FILE, 'w') as f:
    json.dump({"violations": violations}, f, indent=2)

if violations:
    print(f"⚠️ {len(violations)} timing violations detected.")
    for v in violations:
        print(f" - {v['cloud']} too fast: {v['delta']}s < {v['required']}s")
else:
    print("✅ All cloud targets respected timing intervals.")
