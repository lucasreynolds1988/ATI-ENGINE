import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import APIRouter, Request, Header
from backend.utils.auth import validate_token
from agents.web_scraper_agent import run_scraper

router = APIRouter()

@router.post("/scrape/url")
async def scrape_url(request: Request, x_api_token: str = Header(...)):
    if not validate_token(x_api_token):
        return {"error": "Invalid token"}

    data = await request.json()
    url = data.get("url")
    if not url:
        return {"error": "Missing URL"}

    result = run_scraper(url)
    return {"result": result}
