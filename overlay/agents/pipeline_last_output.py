import os

def show_last_final(input_file):
    final_file = f"{input_file}.final.txt"
    if not os.path.isfile(final_file):
        print(f"No final output: {final_file}")
        return
    with open(final_file) as f:
        print(f.read())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        show_last_final(sys.argv[1])
    else:
        print("Usage: python pipeline_last_output.py <input_file>")
