import os

# Token validation (basic)
def validate_token(token: str) -> bool:
    valid_token = os.getenv("API_TOKEN", "")
    return token == valid_token
