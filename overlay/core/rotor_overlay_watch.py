import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class OverlayHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"File created: {event.src_path}")
            subprocess.Popen(["python3", "/home/lucasreynolds1988/Soap/core/rotor_overlay_batch_cloud.py", "upload_gcs"])

    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")

def watch_overlay():
    overlay = os.path.expanduser("~/Soap/overlay")
    event_handler = OverlayHandler()
    observer = Observer()
    observer.schedule(event_handler, overlay, recursive=False)
    observer.start()
    print("Watching overlay for changes. Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch_overlay()

