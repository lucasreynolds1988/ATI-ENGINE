import os

def summary_report(folder):
    files = [f for f in os.listdir(folder) if f.endswith(".final.txt")]
    print(f"Pipeline Summary Report for {folder}:")
    for f in files:
        with open(os.path.join(folder, f)) as file:
            first_line = file.readline().strip()
        print(f"{f}: {first_line}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        summary_report(sys.argv[1])
    else:
        print("Usage: python pipeline_summary_report.py <folder>")
