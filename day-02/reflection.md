# Day 2 — Running and Troubleshooting a Local Server

## Objective
Understand how a server process responds to a request and what happens when it stops.

## Commands I ran
- Start the server: python3 -m http.server 8000 --bind 127.0.0.1
- Request the file:  curl http://127.0.0.1:8000/policy.txt
- Stop the server: CTRL + C 

## What I observed
- Response while the server was running: python3 -m http.server 8000 --bind 127.0.0.1
127.0.0.1 - - [25/Sep/2026 13:44:16] "GET /policy.txt HTTP/1.1" 200 -
Serving HTTP on 127.0.0.1 port 8000 (http://127.0.0.1:8000/)
- Error after I stopped the server: curl: (7) Failed to connect to 127.0.0.1 port 8000 after 2056 ms: Could not connect to server

## What I learned
- A process is: A running program. In this exercise, it was the Python HTTP server.
- A port is: A numbered connection point. The server listened on port 8000.
- The client in this exercise was: curl, which requested policy.txt from the server.
- Stopping the server showed me: The file can still exist, but clients cannot retrieve it through the server when its process is stopped.

## School AI assistant troubleshooting

### Check 1 — Is the application reachable?
- What I would check: Send a request to the application's health endpoint.
- Healthy result: The endpoint responds successfully, such as HTTP 200.
- What a failure might mean: A connection error could mean the server stopped, the address or port is wrong, or something is blocking access. A 404 means I reached a server, but that endpoint wasn't found.

### Check 2 — Is the application's API handling requests?
- What I would check: Send a valid test request to the AI assistant's API endpoint.
- Healthy result: The API accepts the request and returns the expected response format.
- What a failure might mean: A 400 could mean my test request is missing required information or has the wrong format. A server error could mean the application failed while processing it. I would inspect the error and application logs before deciding which.

### Check 3 — Can the application use its AI model provider?
- What I would check: Whether a valid API request can reach the model provider and receive a response; also check for quota or billing errors.
- Healthy result: The provider returns a response and the application can pass it back to the user.
- What a failure might mean: The provider could be unavailable, the credentials could be invalid, or the account could have reached a usage limit. I would use the actual error message to narrow it down.

## Python refresher — Reading a policy file

### What I built
I created `check_policy.py` to read `policy.txt`, print its contents, and count its words.

### Successful run
- Command: `python3 check_policy.py`
- File contents printed: [paste or summarize what appeared]
- Word count: [enter the number your script printed]

### Missing-file test
I temporarily changed the filename in the script to `missing.txt`. Python initially raised a `FileNotFoundError`. After I added `try` and `except FileNotFoundError`, the script printed:

> Could not find the policy file.

I changed the filename back to `policy.txt` and confirmed the successful run still worked.

### What I learned
- `.read()` gets the text from the file.
- `.split()` turns the text into a list of words.
- `len()` counts the items in that list.
- `try` and `except FileNotFoundError` let my program give a useful message when the file is missing.