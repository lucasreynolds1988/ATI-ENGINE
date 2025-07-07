import subprocess
from Soap.core.rotor_overlay import log_event

def run_attention_sequence():
    log_event("+ATTENTION+ STARTED", "INFO")
    subprocess.run(["python3", str(Path.home() / "Soap/core/code_red.py")])
    subprocess.run(["python3", str(Path.home() / "Soap/startup/spin_up.py")])
    log_event("+ATTENTION+ COMPLETE", "SUCCESS")

if __name__ == "__main__":
    run_attention_sequence()
