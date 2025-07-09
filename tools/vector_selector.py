# ~/Soap/tools/vector_selector.py

import os
from core.rotor_overlay import log_event

def select_vector_topic(manual_paths):
    log_event("[VECTOR-SELECTOR] 🧭 Processing user-guided vectors...")

    topics = []
    for path in manual_paths:
        if "electrical" in path.lower():
            topics.append("Electrical Systems")
        elif "axle" in path.lower():
            topics.append("Axles & Suspension")
        elif "hydraulic" in path.lower():
            topics.append("Hydraulics")

    log_event(f"[VECTOR-SELECTOR] 📌 Selected topics: {topics}")
    return topics
