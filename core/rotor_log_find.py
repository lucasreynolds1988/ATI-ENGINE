import os

def find_in_logs(search_term):
    logs_dir = os.path.expanduser("~/Soap/logs")
    found = False
    for f in os.listdir(logs_dir):
        if f.endswith(".log"):
            path = os.path.join(logs_dir, f)
            with open(path, "r") as file:
                for line in file:
                    if search_term in line:
                        print(f"{f}: {line.strip()}")
                        found = True
    if not found:
        print(f"No matches for '{search_term}' in logs.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        find_in_logs(sys.argv[1])
    else:
        print("Usage: python rotor_log_find.py <search_term>")
