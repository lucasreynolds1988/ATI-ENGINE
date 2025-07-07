import os
import zipfile
from core.rotor_overlay import log_event

ZIP_DIR = os.path.expanduser("~/Soap")
LOG_FILE = os.path.expanduser("~/Soap/logs/ziplog_playback.log")

def replay_zip(zip_filename):
    path = os.path.join(ZIP_DIR, zip_filename)
    if not os.path.exists(path):
        log_event(f"ziplog_playback: {zip_filename} not found!")
        return
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(ZIP_DIR)
        log_event(f"ziplog_playback: Extracted {zip_filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        replay_zip(sys.argv[1])
