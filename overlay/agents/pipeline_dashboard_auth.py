import os

API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")

def set_api_token(token):
    with open(API_TOKEN_FILE, "w") as f:
        f.write(token.strip())
    print("API token set.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        set_api_token(sys.argv[1])
    else:
        print("Usage: python pipeline_dashboard_auth.py <token>")
