from fastapi import APIRouter, Request, Header
from backend.utils.auth import validate_token
from backend.agents.soap_phase import run_chat_phase

router = APIRouter()

@router.post("/chat")
async def chat(request: Request, x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}

    data = await request.json()
    user_input = data.get("message")
    if not user_input:
        return {"error": "Missing message"}

    response = run_chat_phase(user_input)
    return {"response": response}
