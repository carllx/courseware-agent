import os
import requests
import json

base_url = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1")
# For cursor API proxies they might use standard anthropic paths or v1/messages
url = f"{base_url}/messages"
if "cursor.scihub.edu.kg" in url:
    # Some proxies require specific paths, we'll try /v1/messages
    url = f"{base_url}/v1/messages"

token = os.environ.get("ANTHROPIC_AUTH_TOKEN", "")
headers = {
    "x-api-key": token,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
    # If the proxy expects Bearer token
    "Authorization": f"Bearer {token}"
}

data = {
    "model": "claude-3-haiku-20240307",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Hello, are you there?"}
    ]
}

resp = requests.post(url, headers=headers, json=data)
print(resp.status_code)
print(resp.text[:500])
