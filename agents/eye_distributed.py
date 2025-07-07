import os
import shutil
import subprocess

def distribute_and_run(input_file, remote_host, remote_dir):
    # Copy file to remote, run supervisor there, pull result back
    base = os.path.basename(input_file)
    remote_path = f"{remote_host}:{remote_dir}/{base}"
    subprocess.run(["scp", input_file, remote_path])
    ssh_cmd = f"cd {remote_dir} && python3 ./agents/pipeline_supervisor.py {base}"
    subprocess.run(["ssh", remote_host, ssh_cmd])
    # Pull back the .final.txt
    final_out = f"{input_file}.final.txt"
    subprocess.run(["scp", f"{remote_host}:{remote_dir}/{base}.final.txt", final_out])
    print(f"Distributed processing complete: {final_out}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        distribute_and_run(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python eye_distributed.py <input_file> <remote_host> <remote_dir>")
