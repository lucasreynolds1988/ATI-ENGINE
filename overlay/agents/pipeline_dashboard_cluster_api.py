from fastapi import FastAPI, Header, HTTPException, Request
import os

app = FastAPI()
API_TOKEN_FILE = os.path.expanduser("~/Soap/secrets/api_token.txt")
CLUSTER_FILE = os.path.expanduser("~/Soap/agents/cluster_nodes.json")

def get_token(x_api_token: str = Header(...)):
    if not os.path.isfile(API_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="API token not set")
    with open(API_TOKEN_FILE) as f:
        correct = f.read().strip()
    if x_api_token != correct:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.get("/cluster/nodes")
def cluster_nodes(x_api_token: str = Header(...)):
    get_token(x_api_token)
    if os.path.isfile(CLUSTER_FILE):
        import json
        with open(CLUSTER_FILE) as f:
            return json.load(f)
    return {"nodes": []}

@app.post("/cluster/nodes")
async def add_node(request: Request, x_api_token: str = Header(...)):
    get_token(x_api_token)
    data = await request.json()
    host = data.get("host")
    if not host:
        raise HTTPException(status_code=400, detail="Host required")
    import json
    nodes = []
    if os.path.isfile(CLUSTER_FILE):
        with open(CLUSTER_FILE) as f:
            nodes = json.load(f).get("nodes", [])
    if host not in nodes:
        nodes.append(host)
    with open(CLUSTER_FILE, "w") as f:
        json.dump({"nodes": nodes}, f)
    return {"status": "added", "host": host}
