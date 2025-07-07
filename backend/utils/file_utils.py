import os

def list_final_files(directory="./upload"):
    return [f for f in os.listdir(directory) if f.endswith(".final.txt")]

def read_final_file(file_id, directory="./upload"):
    path = os.path.join(directory, f"{file_id}.final.txt")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return f.read()
