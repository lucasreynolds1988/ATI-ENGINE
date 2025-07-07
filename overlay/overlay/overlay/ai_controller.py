#!/usr/bin/env python3
import time
from soap_memory import SoapMemory
from arbiter_phase import Arbiter

class AIController:
    def __init__(self):
        self.memory = SoapMemory()
        self.arbiter = Arbiter()

    def generate_sop(self, request):
        print("🧭 Generating SOP for request:", request)
        sop = f"--- SOP Generated ---\nPURPOSE: {request}\n\n[Steps here...]\n"
        self.memory.log_query(request, sop)
        print("✅ SOP generation complete.")
        return sop

    def validate_sop(self, sop):
        conflicts = self.memory.detect_conflicts(sop)
        if conflicts:
            print("⚠️ Conflicts detected. Arbiter phase triggered.")
            self.arbiter.resolve_conflict(conflicts)
        else:
            print("✅ No conflicts found.")

if __name__ == "__main__":
    controller = AIController()
    req = "Brake Adjustment Procedure for 3500lbs Axle"
    sop_text = controller.generate_sop(req)
    print(sop_text)
    controller.validate_sop(sop_text)
