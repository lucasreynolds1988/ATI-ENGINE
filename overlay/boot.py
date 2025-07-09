# ~/Soap/overlay/boot.py

import os
import time
from core.rotor_overlay import log_event

def trigger_boot():
    log_event("🔧 +BOOT+ Triggering system restore chain...")
    open(os.path.expanduser("~/Soap/overlay/.trigger.rebuild"), "w").close()
    time.sleep(1)
    os.system("python3 ~/Soap/overlay/spin_up.py")

if __name__ == "__main__":
    trigger_boot()
