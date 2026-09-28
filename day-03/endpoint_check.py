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
        "url": "http://127.0.0.1:8001/attendance-policy.txt"
    }
]

def check_endpoint(url):
    try:
        response = urlopen(url, timeout=3)

        return {
            "url": url,
            "reachable": True,
            "status": response.status,
            "state": "healthy",
            "error": None
        }

    except HTTPError as error: 
        return {
            "url": url,
            "reachable": True,
            "status": error.code,
            "state": "http_error",
            "error": error.reason
        }
    except URLError as error:
        return {
            "url": url,
            "reachable": False,
            "status": None,
            "state": "url_error",
            "error": error.reason
        }

results = []
for endpoint in endpoints:
    result = check_endpoint(endpoint["url"])
    results.append(result)
    print(result)