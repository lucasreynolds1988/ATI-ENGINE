from fastapi import APIRouter, Header, Response
from fastapi.responses import FileResponse
from backend.utils.auth import validate_token

router = APIRouter()

@router.get("/log")
async def get_log(x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}

    try:
        return FileResponse("backend/logs/rotor_fusion.log", media_type='text/plain', filename="rotor_fusion.log")
    except FileNotFoundError:
        return Response(content="Log not found", status_code=404)
