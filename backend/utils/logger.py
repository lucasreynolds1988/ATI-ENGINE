import datetime

def log_event(message: str, file: str = "backend/logs/rotor_fusion.log"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
