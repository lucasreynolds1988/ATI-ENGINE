#!/usr/bin/env python3
import time
from datetime import datetime
from core.rotor_overlay import log_event
from core.cloud_stream_relay import execute_relay_cycle
from agents.watson_phase import run_watson_phase
from agents.father_phase import run_father_phase
from agents.mother_phase import run_mother_phase
from agents.arbiter_phase import run_arbiter_phase
from agents.soap_phase import run_soap_phase

CYCLE_INTERVAL = 4  # seconds

def rotor_cycle():
    log_event("ROTOR", f"Rotor cycle initiated at {datetime.utcnow().isoformat()}")

    # Execute Eyes relay cycle
    execute_relay_cycle()

    # Execute agent phases sequentially
    run_watson_phase()
    run_father_phase()
    run_mother_phase()
    run_arbiter_phase()
    run_soap_phase()

    log_event("ROTOR", "Rotor cycle complete.")

def main():
    log_event("ROTOR", "Rotor Fusion started.")
    while True:
        rotor_cycle()
        time.sleep(CYCLE_INTERVAL)

if __name__ == "__main__":
    main()
