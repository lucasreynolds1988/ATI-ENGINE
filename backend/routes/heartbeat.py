import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import APIRouter
import time

router = APIRouter()

@router.get("/heartbeat")
async def heartbeat():
    return {
        "alive": True,
        "time": time.time()
    }
