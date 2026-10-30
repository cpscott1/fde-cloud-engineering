# Day 4 — FastAPI API Notes

## Day 4 Objective

Today I moved from using Python's simple static HTTP server to running a real FastAPI application.

The main goal was to understand how a client can send a request to a FastAPI endpoint and receive a JSON response.

My request flow now looks like this:

```text
curl
  ↓
Uvicorn
  ↓
FastAPI
  ↓
Python function
  ↓
JSON response
```

---

# What is FastAPI?

FastAPI is a Python web framework used to build APIs.

Instead of only serving static files, FastAPI lets my Python code decide how the server should respond to different routes.

For example:

```python
@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }
```

This means:

> When a client sends a `GET` request to `/health`, run the `health_check()` function.

---

# What is Uvicorn?

Uvicorn is the server process that runs my FastAPI application and listens for incoming requests.

When I started the app with:

```bash
python3 -m fastapi dev app.py
```

FastAPI started a development server using Uvicorn.

My mental model is:

```text
app.py
  ↓
FastAPI application
  ↓
Uvicorn server
  ↓
listens on 127.0.0.1:8000
  ↓
client sends requests
```

---

# Starting the FastAPI Development Server

I started the application with:

```bash
python3 -m fastapi dev app.py
```

At first, FastAPI could not find the application because it needed a FastAPI app object inside `app.py`.

The important line was:

```python
app = FastAPI()
```

Once the FastAPI application existed, the development server could start successfully.

---

# Health Endpoint

I created:

```text
GET /health
```

and tested it with:

```bash
curl -i http://127.0.0.1:8000/health
```

## Recorded Response

```text
HTTP/1.1 200 OK
date: Mon, 28 Sep 2026 04:56:35 GMT
server: uvicorn
content-length: 15
content-type: application/json

{"status":"ok"}
```

## Interpretation

The FastAPI backend was reachable and successfully responded to the request.

The important evidence was:

```text
HTTP/1.1 200 OK
```

This tells me:

```text
Client reached server       ✅
FastAPI route existed       ✅
Python function ran         ✅
JSON response returned      ✅
```

---

# Documents Endpoint

I also created:

```text
GET /documents
```

I tested it with:

```bash
curl -i http://127.0.0.1:8000/documents
```

## Recorded Response

```text
HTTP/1.1 200 OK
server: uvicorn
content-type: application/json

{"documents":["attendance-policy.txt"]}
```

## Interpretation

The `/documents` endpoint was reachable and returned JSON successfully.

The request flow was:

```text
curl
  ↓
GET /documents
  ↓
Uvicorn
  ↓
FastAPI
  ↓
get_documents()
  ↓
Python dictionary
  ↓
JSON response
```

---

# FastAPI Automatic Documentation

I opened:

```text
http://127.0.0.1:8000/docs
```

and confirmed that both endpoints appeared:

```text
GET /health
GET /documents
```

This showed me that FastAPI automatically generates interactive API documentation from the routes defined in my application.

This can be useful for:

- testing endpoints
- showing customers how an API works
- helping developers understand available routes
- debugging API behavior

---

# Checking Whether the API Process Was Running

I ran:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

## Recorded Output

```text
COMMAND   PID     USER           FD   TYPE   NAME
Python   12421    cameronperry   4u   IPv4   TCP 127.0.0.1:8000 (LISTEN)
Python   12501    cameronperry   4u   IPv4   TCP 127.0.0.1:8000 (LISTEN)
```

## Interpretation

The FastAPI development server was running and listening on:

```text
127.0.0.1:8000
```

The two Python processes are consistent with development reload behavior, where one process may watch for code changes while another serves the application.

The most important evidence was:

```text
(LISTEN)
```

which confirmed that a process was actively waiting for connections on port `8000`.

---

# Customer Troubleshooting Scenario

## Customer Report

The frontend says the backend is unavailable.

## First Check

Command:

```bash
curl -i http://127.0.0.1:8000/health
```

Result:

```text
HTTP/1.1 200 OK
{"status":"ok"}
```

## Is the API Process Running?

Command:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

Result:

```text
Python processes were listening on 127.0.0.1:8000.
```

## Did I Receive an HTTP Response?

Yes.

The `/health` request returned:

```text
200 OK
```

## What Layer Would I Investigate Next?

Because the backend health endpoint is responding successfully, I would not immediately blame the FastAPI service.

I would investigate the next part of the system, such as:

- frontend API URL configuration
- browser request behavior
- frontend code
- CORS
- environment variables
- incorrect route/path
- authentication or authorization
- networking between the frontend and backend

---

# Day 3 vs Day 4

## Day 3

I used:

```bash
python3 -m http.server
```

to serve static files.

The server mainly returned files such as:

```text
attendance-policy.txt
```

The request looked like:

```text
curl
  ↓
static HTTP server
  ↓
file
```

## Day 4

I used FastAPI.

Now my Python code decides what gets returned.

The request looks like:

```text
curl
  ↓
Uvicorn
  ↓
FastAPI route
  ↓
Python function
  ↓
JSON
```

This is a major step toward building a real backend application.

---

# Day 4 Key Takeaways

1. FastAPI is a Python framework for building APIs.
2. Uvicorn runs the FastAPI application and listens for requests.
3. `python3 -m fastapi dev app.py` starts the FastAPI development server.
4. `app = FastAPI()` creates the FastAPI application.
5. `@app.get("/health")` creates a GET request