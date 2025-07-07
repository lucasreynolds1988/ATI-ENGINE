from fastapi import APIRouter
import time

router = APIRouter()

@router.get("/heartbeat")
async def heartbeat():
    return {
        "alive": True,
        "time": time.time()
    }
