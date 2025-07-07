import os
import json
from core.rotor_overlay import log_event

def watson_format(sop_raw):
    """
    Accepts SOP in raw text or dict. Formats to strict Watson template.
    """
    template = {
        "title": "",
        "date": "",
        "version": "1.0",
        "status": "draft",
        "purpose": "",
        "scope": "",
        "safety": [],
        "materials": [],
        "tools": [],
        "procedure": [],
        "troubleshooting": [],
        "maintenance": [],
        "references": [],
        "definitions": []
    }
    # If raw text, try to split into blocks; if dict, merge/clean up
    if isinstance(sop_raw, str):
        # Extremely simple parser: split by headings, fill fields
        for k in template:
            if k in sop_raw.lower():
                idx = sop_raw.lower().find(k)
                val = sop_raw[idx+len(k):].split("\n",1)[-1].strip()
                template[k] = val
    elif isinstance(sop_raw, dict):
        template.update({k: sop_raw.get(k, template[k]) for k in template})
    return template

def process(input_path, output_path):
    with open(input_path) as f:
        raw = f.read()
        try:
            sop_raw = json.loads(raw)
        except Exception:
            sop_raw = raw
    sop = watson_format(sop_raw)
    with open(output_path, "w") as f:
        json.dump(sop, f, indent=2)
    log_event(f"Watson: SOP formatted and written to {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        process(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python watson_phase.py <input_file> <output_file>")
