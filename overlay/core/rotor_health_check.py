import os
from core.rotor_overlay import log_event

def check_rotor_files():
    core_files = [
        "spin_up.py", "spin_down.py", "rotor_fusion.py", "fusion_restore_v2.py",
        "code_red.py", "attention.py", "rotor_overlay.py", "cloud_stream_relay.py",
        "mongo_safe_upload_v2.py"
    ]
    missing = []
    core_dir = os.path.expanduser("~/Soap/core")
    for f in core_files:
        if not os.path.exists(os.path.join(core_dir, f)):
            missing.append(f)
    if missing:
        log_event(f"rotor_health_check: MISSING files: {', '.join(missing)}")
    else:
        log_event("rotor_health_check: All rotor files present and correct.")

if __name__ == "__main__":
    check_rotor_files()
