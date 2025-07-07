#!/usr/bin/env python3
import difflib

def resolve_conflict(text1, text2):
    diff = difflib.unified_diff(text1.splitlines(), text2.splitlines(), lineterm='')
    return "\n".join(diff)

if __name__ == "__main__":
    a = "Step 1: Disconnect power"
    b = "Step 1: Shut off power"
    print(resolve_conflict(a, b))
