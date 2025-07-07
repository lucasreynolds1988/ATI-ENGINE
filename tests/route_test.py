import requests

def test_ping():
    r = requests.get("http://localhost:8000/ping")
    assert r.status_code == 200
    print("✅ /ping OK")

if __name__ == "__main__":
    test_ping()
