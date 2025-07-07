import os
from core.rotor_overlay import log_event

def safety_check():
    # Example: Make sure secrets are present and protected
    secrets_dir = os.path.expanduser("~/Soap/secrets")
    expected = ["gcs-creds.json", "github-token.txt", "mongo-creds.txt"]
    missing = []
    for f in expected:
        if not os.path.isfile(os.path.join(secrets_dir, f)):
            missing.append(f)
    if missing:
        log_event(f"rotor_safety_check: Missing secret(s): {', '.join(missing)}")
    else:
        log_event("rotor_safety_check: All secrets present.")

if __name__ == "__main__":
    safety_check()
