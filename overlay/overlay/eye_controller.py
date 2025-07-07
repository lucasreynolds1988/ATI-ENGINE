#!/usr/bin/env python3
import threading
import time
from virtual_cache_relay import VirtualCacheRelay

class EyeController:
    def __init__(self):
        self.relay = VirtualCacheRelay()
        self.running = True

    def spawn_eyes(self, num_eyes=3):
        print(f"🧭 Spawning {num_eyes} Eyes for circulation.")
        for i in range(num_eyes):
            threading.Thread(target=self.eye_loop, args=(i,), daemon=True).start()

    def eye_loop(self, eye_id):
        while self.running:
            print(f"👁️ Eye {eye_id} active. Passing chunk.")
            time.sleep(4)

    def load_data(self, chunks):
        self.relay.load_chunks(chunks)

    def shutdown(self):
        print("⚠️ EyeController shutting down.")
        self.running = False

if __name__ == "__main__":
    controller = EyeController()
    controller.load_data(["Manual_Page_1", "Manual_Page_2", "Manual_Page_3"])
    controller.spawn_eyes(3)

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        controller.shutdown()
