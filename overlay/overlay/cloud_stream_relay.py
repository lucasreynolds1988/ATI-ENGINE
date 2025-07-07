#!/usr/bin/env python3
import time

def stream_data_to_eye(data):
    print("🧭 Streaming data to Eye for 1 second...")
    time.sleep(1)
    print(f"✅ Eye read complete: {data[:30]}...")

def relay_loop():
    print("🧭 Cloud Stream Relay ONLINE. Circulating data between Eyes.")
    data_chunks = ["ChunkA", "ChunkB", "ChunkC"]
    while True:
        for chunk in data_chunks:
            stream_data_to_eye(chunk)
            time.sleep(3)  # maintain 4s cycle with 1s stream
        print("🔄 Loop complete. Restarting data circulation.")

if __name__ == "__main__":
    relay_loop()
