# ~/Soap/soap_phase.py

"""
Soap Phase — Final Oracle SOP Response Engine
Consumes structured SOPs and returns a clean, human-readable breakdown.
"""

import json
from pathlib import Path

QUEUE_DIR = Path.home() / "Soap" / "agent_queue"
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

def explain_sop(sop):
    tech_notes = []
    breakdown = []

    # Title and status
    breakdown.append(f"📌 Title: {sop.get('title', 'N/A')}")
    breakdown.append(f"📅 Date: {sop.get('date', 'N/A')}")
    breakdown.append(f"🔢 Version: {sop.get('version', 'N/A')}")
    breakdown.append(f"📋 Status: {sop.get('status', 'N/A')}")
    breakdown.append("")

    # Purpose and Scope
    breakdown.append(f"🎯 Purpose: {sop.get('purpose', '').strip()}")
    breakdown.append(f"🧭 Scope: {sop.get('scope', '').strip()}")
    breakdown.append("")

    # Tools
    breakdown.append("🧰 Required Tools:")
    for tool in sop.get("tools", []):
        breakdown.append(f"  - {tool}")
    breakdown.append("")

    # Materials
    breakdown.append("📦 Required Materials:")
    for mat in sop.get("materials", []):
        breakdown.append(f"  - {mat}")
    breakdown.append("")

    # Safety
    breakdown.append("⚠️ Safety Notices:")
    for safe in sop.get("safety", []):
        breakdown.append(f"  - {safe}")
    breakdown.append("")

    # Procedure
    for section in sop.get("procedure", []):
        breakdown.append(f"🔧 {section.get('title', 'Unnamed Section')}")
        for step in section.get("steps", []):
            breakdown.append(f"  - {step}")
        breakdown.append("")

    # Maintenance Schedule
    if "maintenance" in sop:
        breakdown.append("🛠️ Maintenance Schedule:")
        for item in sop["maintenance"]:
            breakdown.append(f"  - {item}")
        breakdown.append("")

    # Troubleshooting
    if "troubleshooting" in sop:
        breakdown.append("🧩 Troubleshooting:")
        for t in sop["troubleshooting"]:
            breakdown.append(f"  - {t}")
        breakdown.append("")

    # References
    if "references" in sop:
        breakdown.append("📚 References:")
        for r in sop["references"]:
            breakdown.append(f"  - {r}")
        breakdown.append("")

    return {
        "explanation": breakdown,
        "tech_notes": sop.get("tech_notes", []),
        "conflicts": sop.get("conflicts", [])
    }

def main():
    # Simulate getting latest SOP file (or use agent queue later)
    latest_file = QUEUE_DIR / "latest_sop.json"
    if not latest_file.exists():
        print(json.dumps({"error": "No SOP available"}))
        return

    with open(latest_file, "r", encoding="utf-8") as f:
        sop = json.load(f)

    response = explain_sop(sop)
    response["status"] = "soap_complete"
    print(json.dumps(response))

if __name__ == "__main__":
    main()
