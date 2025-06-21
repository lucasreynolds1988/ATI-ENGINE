# ~/Soap/cloud_stream_relay.py

import os
import time
import threading
import hashlib
from pymongo import MongoClient
from bson.binary import Binary
import subprocess

# === ROTOR CLOCK ===
class RotorClock:
    def __init__(self, interval=4):
        self.interval = interval
        self.last_tick = time.time()

    def wait_for_next(self):
        now = time.time()
        sleep_time = max(0, self.interval - (now - self.last_tick))
        time.sleep(sleep_time)
        self.last_tick = time.time()

# === CONFIG ===
MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"
DB = MongoClient(MONGO_URI).fusion
GCS_BUCKET = "gs://ati-rotor-fusion"

# === CORE STREAM BUFFER ===
buffer = []
buffer_lock = threading.Lock()

def read_stream():
    print("🔁 [Input] Waiting for incoming code stream...")
    while True:
        line = input()
        with buffer_lock:
            buffer.append(line)
        if line.strip() == "#EOF":
            break

def rotor_push(clock):
    print("🚀 [Rotor] Starting transmission relay...")
    chunk_index = 0
    while True:
        with buffer_lock:
            if not buffer:
                time.sleep(1)
                continue
            chunk_data = "\n".join(buffer).encode()
            file_hash = hashlib.sha256(chunk_data).hexdigest()

        # Mongo Upload
        clock.wait_for_next()
        DB.file_chunks.insert_one({
            "chunk_id": f"{file_hash}_{chunk_index}",
            "data": Binary(chunk_data),
            "index": chunk_index,
            "origin": "relay"
        })
        print(f"🛰️ Mongo chunk {chunk_index} pushed")

        # GCS Upload
        clock.wait_for_next()
        temp_path = f"/tmp/{file_hash}_{chunk_index}.py"
        with open(temp_path, "wb") as f:
            f.write(chunk_data)
        os.system(f"gsutil cp {temp_path} {GCS_BUCKET}/stream/{file_hash}_{chunk_index}.py")
        os.remove(temp_path)
        print(f"☁️ GCS chunk {chunk_index} pushed")

        break  # Send once per session for now

def rotor_pull_and_run():
    print("🔄 [Rotor] Attempting remote reconstruction...")
    doc = DB.file_chunks.find_one({"origin": "relay"}, sort=[("index", 1)])
    if not doc:
        print("⚠️ No chunks found.")
        return

    code = doc["data"].decode()
    if "#RUNTIME" in code:
        print("🚦 [EXEC] Running suspended memory stream...")
        exec(code, globals())
    else:
        print("📜 [RECV] Code received, but no #RUNTIME tag found.")

def start_relay():
    clock = RotorClock()
    t1 = threading.Thread(target=read_stream)
    t2 = threading.Thread(target=rotor_push, args=(clock,))
    t3 = threading.Thread(target=rotor_pull_and_run)

    t1.start()
    t1.join()
    t2.start()
    t2.join()
    t3.start()
    t3.join()

if __name__ == "__main__":
    start_relay()
