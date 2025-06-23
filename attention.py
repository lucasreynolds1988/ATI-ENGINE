#!/usr/bin/env python3
"""
Attention module: System wake-up trigger for ATI Rotor Fusion.
Creates and handles the .trigger.rebuild file, logs wake-up events,
and emits a cognitive pulse before handing off to Rotor Fusion.
"""

import os
import sys
import time
from pathlib import Path

# Configuration
HOME_DIR = Path.home()
SOAP_DIR = HOME_DIR / "Soap"
LOG_DIR = SOAP_DIR / "data" / "logs"
TRIGGER_FILE = SOAP_DIR / ".trigger.rebuild"
WAKE_LOG = LOG_DIR / "attention.log"
PULSE_COUNT = 3
PULSE_INTERVAL = 1  # seconds between pulses

def ensure_log_dir():
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"⚠️ Could not create log directory {LOG_DIR}: {e}", file=sys.stderr)

def log_event(message: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry)
    try:
        with open(WAKE_LOG, "a") as f:
            f.write(entry + "\n")
    except Exception as e:
        print(f"⚠️ Failed to write to log {WAKE_LOG}: {e}", file=sys.stderr)

def handle_trigger_file():
    if TRIGGER_FILE.exists():
        log_event(f"Detected trigger file: {TRIGGER_FILE}")
        try:
            TRIGGER_FILE.unlink()
            log_event(f"Removed trigger file.")
        except Exception as e:
            log_event(f"Could not remove trigger file: {e}")
    else:
        log_event("No trigger file found; proceeding without cleanup.")

def emit_cognitive_pulse(count: int, interval: float):
    for i in range(count):
        print("🧠 Cognitive pulse...")
        time.sleep(interval)
    log_event(f"Emitted {count} cognitive pulses.")

def main():
    ensure_log_dir()
    log_event("[ATTENTION] System wake-up initiated.")
    handle_trigger_file()
    emit_cognitive_pulse(PULSE_COUNT, PULSE_INTERVAL)
    log_event("Attention module online. Handing off to Rotor Fusion.")

if __name__ == "__main__":
    main()
