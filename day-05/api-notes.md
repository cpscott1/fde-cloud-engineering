# Day 5 — FastAPI POST Requests and Pydantic Validation

## Day 5 Objective

Today I moved from only retrieving information with `GET` requests to sending structured data into my FastAPI application with a `POST` request.

The main concepts were:

- `GET` vs `POST`
- request bodies
- JSON
- Pydantic schemas
- API validation
- HTTP `200`
- HTTP `404`
- HTTP `422`
- troubleshooting API contracts

The request flow I am learning is:

```text
Client
  ↓
HTTP request
  ↓
FastAPI
  ↓
Pydantic validation
  ↓
Python function
  ↓
JSON response
```

---

# Virtual Environment Setup

When I first tried to run FastAPI, Python returned:

```text
No module named fastapi
```

The Python interpreter being used was different from the one where FastAPI had previously been installed.

I created and activated a project virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then installed FastAPI inside the virtual environment.

I verified the FastAPI CLI with:

```bash
python -m fastapi --help
```

The terminal prompt showed:

```text
(.venv)
```

This confirmed that the project-specific Python environment was active.

## Why This Matters

A virtual environment helps keep the project's Python packages separate from other Python installations on my computer.

Mental model:

```text
Mac
  ↓
fde-cloud-engineering
  ↓
.venv
  ↓
project Python
  ↓
FastAPI
Pydantic
Uvicorn
```

---

# Day 5 FastAPI Server

From the `day-05` folder, I started the development server with:

```bash
python -m fastapi dev app.py
```

The FastAPI application ran locally on:

```text
http://127.0.0.1:8000
```

---

# Health Endpoint Test

I tested:

```bash
curl -i http://127.0.0.1:8000/health
```

## Recorded Response

```text
HTTP/1.1 200 OK
server: uvicorn
content-type: application/json

{"status":"ok"}
```

## Interpretation

The FastAPI backend was reachable and responding successfully.

```text
Reached server       ✅
Route existed        ✅
Function ran         ✅
JSON returned        ✅
```

---

# Documents Endpoint Test

I tested:

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

This established that the Day 5 backend was healthy before testing the new POST endpoint.

---

# GET vs POST

## GET

I use `GET` when the client wants to retrieve information.

Examples:

```text
GET /health
GET /documents
```

Simple mental model:

```text
GET
↓
"Give me information."
```

---

## POST

I use `POST` when the client wants to send information to the application for processing.

Example:

```text
POST /ask
```

Simple mental model:

```text
POST
↓
"Here is information for you to process."
```

For the B2D Cloud AI Knowledge Assistant:

```text
Student question
  ↓
POST /ask
  ↓
FastAPI
  ↓
eventually RAG + LLM
  ↓
answer
```

---

# What is a Request Body?

A request body contains data being sent to the API.

For example:

```json
{
  "question": "What is the attendance policy?"
}
```

This JSON is sent inside the POST request.

Mental model:

```text
POST /ask
     +
request body
     ↓
{
  "question": "What is the attendance policy?"
}
```

---

# Pydantic Schema

I used Pydantic to define the structure expected by the API.

Example:

```python
from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str
```

This tells the application:

```text
Expected field:
question

Expected type:
string
```

A valid request looks like:

```json
{
  "question": "What is the attendance policy?"
}
```

A request using a different field name does not match the schema.

---

# First `/ask` Test — Route Not Found

My first attempt to send a POST request was:

```bash
curl -i \
  -X POST \
  http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the attendance policy?"}'
```

## Recorded Response

```text
HTTP/1.1 404 Not Found

{"detail":"Not Found"}
```

## Interpretation

The server was reachable because FastAPI returned an HTTP response.

However, FastAPI did not yet have a matching:

```text
POST /ask
```

route.

This was not a Pydantic validation problem yet.

The request flow stopped here:

```text
curl
  ↓
FastAPI reached ✅
  ↓
POST /ask route found ❌
```

This connected back to my Day 3 troubleshooting lesson:

> **How far did the request get?**

---

# Successful `/ask` Request

After adding the `/ask` route, I tested again:

```bash
curl -i \
  -X POST \
  http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the attendance policy?"}'
```

## Recorded Response

```text
HTTP/1.1 200 OK
server: uvicorn
content-type: application/json
```

Response body:

```json
{
  "question": "What is the attendance policy?",
  "answer": "AI answer will go here later"
}
```

## Interpretation

This time:

```text
Client reached FastAPI        ✅
POST /ask route existed       ✅
Request body was valid        ✅
Pydantic validation passed    ✅
Python function ran           ✅
JSON response returned        ✅
```

The complete flow was:

```text
curl
  ↓
POST /ask
  ↓
JSON request body
  ↓
Pydantic
  ↓
QuestionRequest
  ↓
ask_question()
  ↓
Python dictionary
  ↓
JSON response
```

---

# Invalid Request Test

Next I intentionally sent the wrong field name.

The API expects:

```json
{
  "question": "What is the attendance policy?"
}
```

But I sent:

```json
{
  "prompt": "What is the attendance policy?"
}
```

Command:

```bash
curl -i \
  -X POST \
  http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt":"What is the attendance policy?"}'
```

## Recorded Response

```text
HTTP/1.1 422 Unprocessable Content
```

FastAPI returned:

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "question"
      ],
      "msg": "Field required",
      "input": {
        "prompt": "What is the attendance policy?"
      }
    }
  ]
}
```

---

# Understanding the `422` Response

The important information was:

```text
type: missing
```

This means a required field was missing.

```text
loc: ["body", "question"]
```

This means the problem occurred in the request body and specifically involved the `question` field.

```text
msg: "Field required"
```

This tells me Pydantic expected a field called:

```text
question
```

but did not receive it.

The actual request contained:

```text
prompt
```

instead.

---

# What the `422` Proved

The server itself was not down.

The route was not missing.

The request successfully reached FastAPI.

The failure happened during input validation.

```text
Server reachable        ✅
POST /ask exists        ✅
Request reached API     ✅
Schema matched          ❌
Pydantic validation     ❌
```

This is very different from the earlier `404`.

---

# Comparing the Day 5 HTTP Results

## `200 OK`

```text
Request reached server
↓
Route existed
↓
Request matched schema
↓
Function ran
↓
Successful response
```

## `404 Not Found`

```text
Request reached server
↓
Requested route did not exist
```

## `422 Unprocessable Content`

```text
Request reached server
↓
Route existed
↓
Request body did not match expected schema
↓
Validation rejected request
```

---

# API Contract

I learned that an API has an expected contract between the client and server.

For `/ask`, the contract currently expects:

```json
{
  "question": "some text"
}
```

If the frontend sends:

```json
{
  "prompt": "some text"
}
```

the client and server disagree about the contract.

That mismatch causes validation to fail.

---

# FDE Customer Scenario

Imagine a school district says:

> “Our frontend cannot send student questions to the B2D Knowledge Assistant.”

The frontend sends:

```json
{
  "prompt": "What is the attendance policy?"
}
```

But the backend expects:

```json
{
  "question": "What is the attendance policy?"
}
```

The backend returns:

```text
422 Unprocessable Content
```

## My Investigation

### Is the backend running?

Yes.

Evidence:

```text
GET /health → 200 OK
```

### Does the `/ask` route exist?

Yes.

Evidence:

A valid POST request returned:

```text
200 OK
```

### Is this an AI model failure?

No.

The request failed before any AI model was called.

### What actually failed?

The request body did not match the Pydantic schema.

### Recommended Fix

The frontend should send:

```json
{
  "question": "What is the attendance policy?"
}
```

instead of:

```json
{
  "prompt": "What is the attendance policy?"
}
```

---

# FDE Troubleshooting Mental Model

A customer may report:

> “The AI app is broken.”

But there are multiple possible failure points:

```text
Client
  ↓
Network
  ↓
FastAPI server
  ↓
Route
  ↓
Pydantic validation
  ↓
Application logic
  ↓
RAG
  ↓
LLM
```

Today's problem happened here:

```text
Pydantic validation
```

The request never reached an AI model.

This reinforces the question:

> **How far did the request get?**

---

# Important Day 5 Concepts

## Route

A route connects an HTTP method and path to Python code.

Example:

```python
@app.post("/ask")
```

---

## Request Body

The data sent into the API.

Example:

```json
{
  "question": "What is the attendance policy?"
}
```

---

## Schema

The expected structure of the data.

Example:

```python
class QuestionRequest(BaseModel):
    question: str
```

---

## Validation

Checking whether incoming data matches the expected schema.

---

## Serialization

FastAPI converts supported Python return data into JSON for the HTTP response.

---

# Day 5 Key Takeaways

1. `GET` usually retrieves information.
2. `POST` can send information to an API for processing.
3. A POST request can contain a request body.
4. JSON is commonly used to send structured API data.
5. Pydantic defines and validates expected data structures.
6. `question: str` means the request should contain a `question` field with a string value.
7. `200 OK` means the request succeeded.
8. `404 Not Found` can mean the requested route does not exist.
9. `422 Unprocessable Content` means FastAPI understood the request but validation failed.
10. A healthy backend can still reject a bad request.
11. API clients and servers must agree on an API contract.
12. Validation errors can happen before application logic or an AI model is reached.
13. An FDE should identify the exact failure layer instead of blaming the whole application.
14. The question “How far did the request get?” continues to be useful.

---

# Day 5 Verified Progress

- [x] Created Day 5 project files
- [x] Created and activated `.venv`
- [x] Installed FastAPI in the virtual environment
- [x] Verified FastAPI CLI
- [x] Started the Day 5 FastAPI server
- [x] Verified `GET /health`
- [x] Verified `GET /documents`
- [x] Created Pydantic `QuestionRequest`
- [x] Created `POST /ask`
- [x] Observed an initial `404` when the route was missing
- [x] Successfully sent a valid POST request
- [x] Received `200 OK`
- [x] Successfully received JSON from `/ask`
- [x] Intentionally sent an invalid request
- [x] Received `422 Unprocessable Content`
- [x] Identified the missing `question` field
- [x] Distinguished server health from validation failure

---

# Still To Complete

The following Day 5 work has not yet been verified:

- [ ] Test an empty JSON object: `{}` 
- [ ] Test an empty question string: `{"question": ""}`
- [ ] Complete `customer-scenario.md`
- [ ] Complete the Day 5 Python refresher
- [ ] Complete `reflection.md`

---

# Next Step Toward the B2D Cloud AI Knowledge Assistant

The application can now accept a student question:

```text
POST /ask
```

Current flow:

```text
Student
  ↓
question
  ↓
FastAPI
  ↓
Pydantic validation
  ↓
placeholder answer
```

The future flow will become:

```text
Student
  ↓
question
  ↓
FastAPI
  ↓
Pydantic validation
  ↓
retrieve relevant school documents
  ↓
RAG context
  ↓
LLM
  ↓
answer
```

The next major engineering step is to begin retrieving relevant information from local knowledge documents before introducing a model.