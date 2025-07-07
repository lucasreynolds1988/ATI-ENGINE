import os
import json

AGENTS_DIR = os.path.expanduser("~/Soap/agents")

def docgen(outfile="PIPELINE_DOC.md"):
    lines = []
    for fname in os.listdir(AGENTS_DIR):
        if fname.endswith(".py"):
            with open(os.path.join(AGENTS_DIR, fname)) as f:
                first = f.readline()
                if first.startswith('"""'):
                    doc = first.strip('"""\n').strip()
                    lines.append(f"## {fname}\n{doc}\n")
    with open(outfile, "w") as f:
        f.writelines(lines)
    print(f"Generated {outfile}")

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "PIPELINE_DOC.md"
    docgen(out)
