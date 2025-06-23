# ~/Soap/status_lights.py

import os
import time
import curses
import subprocess
from pathlib import Path

LOG_PATH = Path.home() / "Soap/logs/restore.log"

def check_process(keyword):
    try:
        result = subprocess.check_output(f"pgrep -f {keyword}", shell=True)
        return bool(result.strip())
    except subprocess.CalledProcessError:
        return False

def draw_status(screen):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # GitHub
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # MongoDB
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)   # GCS
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)    # Rotor engine

    while True:
        screen.clear()
        screen.border(0)

        screen.addstr(0, 2, "ATI FUSION MONITOR 🧠", curses.A_BOLD)
        screen.addstr(2, 4, "[System Status Lights]", curses.A_UNDERLINE)

        github = check_process("boot.py") or "Pulling latest from GitHub" in LOG_PATH.read_text()
        mongo  = "Fetching chunked files from MongoDB" in LOG_PATH.read_text()
        gcs    = "Syncing from GCS overlay" in LOG_PATH.read_text()
        rotor  = any(check_process(x) for x in ["rotor_overlay", "rotor_fusion", "fusion_restore_v2"])

        screen.addstr(4, 6, "🔵 GitHub Pull: ", curses.color_pair(1 if github else 0))
        screen.addstr("ONLINE" if github else "OFFLINE", curses.color_pair(1 if github else 0))

        screen.addstr(5, 6, "🟣 MongoDB Ingest: ", curses.color_pair(2 if mongo else 0))
        screen.addstr("ACTIVE" if mongo else "IDLE", curses.color_pair(2 if mongo else 0))

        screen.addstr(6, 6, "🔴 GCS Overlay: ", curses.color_pair(3 if gcs else 0))
        screen.addstr("SYNCED" if gcs else "WAITING", curses.color_pair(3 if gcs else 0))

        screen.addstr(7, 6, "🟢 Rotor Engine: ", curses.color_pair(4 if rotor else 0))
        screen.addstr("SPINNING" if rotor else "STOPPED", curses.color_pair(4 if rotor else 0))

        screen.addstr(9, 4, "Press CTRL+C to exit", curses.A_DIM)

        screen.refresh()
        time.sleep(3)

def main():
    curses.wrapper(draw_status)

if __name__ == "__main__":
    main()
