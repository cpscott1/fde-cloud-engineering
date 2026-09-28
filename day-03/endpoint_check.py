from urllib.request import urlopen
from urllib.error import HTTPError, URLError

endpoints = [
    {
        "name": "primary-policy",
        "url": "http://127.0.0.1:8000/attendance-policy.txt"
    },
    {
        "name": "missing-policy",
        "url": "http://127.0.0.1:8000/missing-policy.txt"
    },
    {
        "name": "alternate-policy",
        "url": "http://127.0.0.1:8000/attendance-policy.txt"
    }
]

def check_endpoint(url):
    response = urlopen(url, timeout=3)
    return {
        "url": url,
        "result": response,
        "status": response.status
    }