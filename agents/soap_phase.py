# ~/Soap/agents/soap_phase.py

import json
from pathlib import Path
import os

QUEUE_DIR = Path.home() / "Soap/agent_queue"
os.makedirs(QUEUE_DIR, exist_ok=True)

def explain_sop(sop):
    tech_notes = []
    breakdown = []

    # Explain purpose and scope
    breakdown.append(f"📌 This SOP is for: {sop.get('purpose', '').strip()}")
    breakdown.append(f"📍 It applies to: {sop.get('scope', '').strip()}")

    # Tools and Materials
    breakdown.append("🧰 Tools needed:")
    for tool in sop.get("tools", []):
        breakdown.append(f"  - {tool}")

    breakdown.append("📦 Materials needed:")
    for mat in sop.get("materials", []):
        breakdown.append(f"  - {mat}")

    # Safety Notes
    if sop.get("safety"):
        breakdown.append("🛡️ Safety notes:")
        for note in sop["safety"]:
            breakdown.append(f"  ⚠️ {note}")

    # Procedure explained
    breakdown.append("🛠️ Step-by-step breakdown:")
    for i, step in enumerate(sop.get("procedure", []), start=1):
        breakdown.append(f"  Step {i}: {step}")

        if any(keyword in step.lower() for keyword in ["remove", "disassemble"]):
            tech_notes.append(f"Step {i} involves disassembly — ensure all parts are clean and tracked.")
        if any(keyword in step.lower() for keyword in ["torque", "tighten"]):
            tech_notes.append(f"Step {i} involves fasteners — use a torque wrench as specified.")
        if "grease" in step.lower():
            tech_notes.append(f"Step {i}: Ensure correct type and amount of grease is used.")

    return breakdown, tech_notes

def run_soap():
    tasks = sorted(QUEUE_DIR.glob("*.json"))
    for task in tasks:
        with open(task, "r") as f:
            data = json.load(f)

        if data.get("status") != "fully_verified":
            continue

        print(f"🧽 Soap explaining: {task.name}")
        breakdown, tech_notes = explain_sop(data)

        data["status"] = "soap_complete"
        data["explanation"] = breakdown
        data["tech_notes"] = tech_notes

        with open(task, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Explanation complete: {task.name}")

if __name__ == "__main__":
    run_soap()
