# ~/Soap/backend/routes/agents.py

from fastapi import APIRouter, Request
from agents.soap_phase import synthesize_final_sop

router = APIRouter()

@router.post("/sop/synthesize")
async def sop_synthesize(request: Request):
    data = await request.json()
    result = synthesize_final_sop(data)
    return result
