#!/usr/bin/env python3
import requests

file_path = "sample_manual.pdf"
url = "http://localhost:3000/manuals/upload"
token = "SUPERSECRET123"

with open(file_path, "rb") as f:
    files = {"file": (file_path, f, "application/pdf")}
    headers = {"x-api-token": token}
    response = requests.post(url, files=files, headers=headers)

print(response.json())
