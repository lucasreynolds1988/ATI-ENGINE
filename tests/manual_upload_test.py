import requests

def test_upload():
    with open("sample_manual.txt", "rb") as f:
        files = {"file": ("sample_manual.txt", f)}
        r = requests.post("http://localhost:8000/manuals/upload", files=files)
        print(r.json())

if __name__ == "__main__":
    test_upload()
