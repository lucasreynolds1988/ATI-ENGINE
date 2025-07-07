from fastapi import APIRouter, Header, Request
from backend.utils.auth import validate_token
from backend.pipeline_runner import run_pipeline_job

router = APIRouter()

@router.post("/synthesize")
async def synthesize(request: Request, x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}

    data = await request.json()
    file_id = data.get("file_id")
    if not file_id:
        return {"error": "Missing file_id"}

    result = run_pipeline_job(file_id)
    return {"result": result}
