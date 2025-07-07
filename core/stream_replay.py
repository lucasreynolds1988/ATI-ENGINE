def replay_log(log_path):
    try:
        with open(log_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                print("[REPLAY]", line.strip())
    except FileNotFoundError:
        print("Log file not found:", log_path)
