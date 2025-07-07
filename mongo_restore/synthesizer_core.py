from typing import List
import datetime
import uuid

# === Agent Stubs ===
from agents.formatting_watson import Watson
from agents.safety_mother import Mother
from agents.logic_father import Father

# === SOP Output Model ===
from models.sop_template import SOPTemplate

# === Main Synthesis Function ===
def synthesize_sop(manual_title: str, text_chunks: List[str]) -> SOPTemplate:
    """
    Full SOP generation pipeline using Watson, Mother, and Father personas.
    """
    print(f"[🧠 SYNTHESIZER] Starting SOP synthesis for: {manual_title}")

    # Step 1: Formatting
    print("[🧠 Watson] Formatting raw manual text...")
    formatted_sections = Watson.format_sections(text_chunks)

    # Step 2: Safety
    print("[🛡️ Mother] Injecting safety protocols...")
    safe_sections = Mother.enforce_safety(formatted_sections)

    # Step 3: Logic + Structure
    print("[📐 Father] Structuring final SOP with logic and metadata...")
    final_sop = Father.build_sop(
        title=manual_title,
        sections=safe_sections,
        created_by="ATI Fusion Engine",
        created_at=datetime.datetime.now().isoformat(),
        sop_id=str(uuid.uuid4())
    )

    print("[✅ COMPLETE] SOP synthesis done.")
    return final_sop
