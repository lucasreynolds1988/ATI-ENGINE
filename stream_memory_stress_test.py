# ~/Soap/stream_memory_stress_test.py

import os
import time
import threading
import psutil
import gzip
import random
import string
import tempfile
from datetime import datetime

# === CONFIG ===
MAX_MEMORY_MB = 200  # Max simulated memory use
CHUNK_SIZE_KB = 512  # Each chunk ~512KB uncompressed
SIM_DURATION = 60    # How long to run the stress test (seconds)
NUM_THREADS = 5      # Parallel streams
USE_RUNTIME = True

def generate_large_payload():
    body = ''.join(random.choices(string.ascii_letters + string.digits, k=CHUNK_SIZE_KB * 1024))
    if USE_RUNTIME:
        body += "\n#RUNTIME\nprint(\"Executed under pressure\")"
    return body.encode("utf-8")

def compress_and_discard(data):
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        with gzip.open(tmp.name, 'wb') as f:
            f.write(data)
        # simulate cloud push delay
        time.sleep(random.uniform(0.1, 0.3))

def stream_loop(label):
    print(f"[🔥] Starting thread: {label}")
    end_time = time.time() + SIM_DURATION
    count = 0
    while time.time() < end_time:
        payload = generate_large_payload()
        compress_and_discard(payload)
        count += 1
        mem = psutil.virtual_memory().used / (1024*1024)
        print(f"[{label}] Payload {count} | Memory: {mem:.1f}MB")
    print(f"[✅] Thread {label} complete")

# === MAIN ===
print("🧪 Starting stream memory stress test...")
threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=stream_loop, args=(f"T{i+1}",))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("✅ Stress test complete. Check for rotor bottlenecks or logs under pressure.")
