from arbiter_phase import apply_arbiter_to_sections

def test_conflict_output():
    sample = {
        "tools": ["Wrench\nHammer", "Hammer\nWrench"],
        "safety": ["Wear gloves", "Wear gloves and goggles"]
    }
    resolved = apply_arbiter_to_sections(sample)
    for key, val in resolved.items():
        print(f"--- {key.upper()} ---\n{val}\n")

if __name__ == "__main__":
    test_conflict_output()
