from fastapi import APIRouter, Request, Header
from backend.utils.auth import validate_token
from agents.watson_phase import process as watson_process
from agents.soap_phase import soap_finalize
import os
import uuid

router = APIRouter()

@router.post("/sop/generate")
async def generate_sop(request: Request, x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}

    body = await request.body()
    temp_id = str(uuid.uuid4())
    input_path = f"/tmp/{temp_id}_raw.json"
    formatted_path = f"/tmp/{temp_id}_watson.json"
    final_path = f"/tmp/{temp_id}_final.txt"

    with open(input_path, "wb") as f:
        f.write(body)

    watson_process(input_path, formatted_path)
    soap_finalize(formatted_path, final_path)

    with open(final_path) as f:
        result = f.read()

    return {"sop_output": result}
