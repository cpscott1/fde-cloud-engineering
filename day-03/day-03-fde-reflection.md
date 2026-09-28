# Day 3 — Networking, HTTP Troubleshooting, and Python Health Checks

## Day 3 Objective

Today I focused on understanding how a client reaches a service, how HTTP responses help diagnose problems, and how to automate those checks with Python.

The biggest theme of the day was:

> **How far did my request get?**

Instead of assuming that an application, server, network, or AI model is broken, I learned to use evidence to determine which part of the system actually failed.

---

# 1. Core Networking Concepts I Learned

## What is `curl`?

`curl` is a command-line tool that sends a request to a service and shows the response.

For example:

```bash
curl -i http://127.0.0.1:8000/attendance-policy.txt
```

This means:

- `curl` — send a request
- `-i` — include HTTP response headers
- `127.0.0.1` — my own computer
- `8000` — the port where the service is listening
- `attendance-policy.txt` — the resource I am requesting

A useful mental model is:

```text
curl
  ↓
send request
  ↓
server
  ↓
send response
  ↓
curl displays response
```

`curl` acts as the **client**.

The Python HTTP server acts as the **server**.

---

## Client vs. Server

A client asks for something.

A server listens for requests and responds.

During this exercise, both were running on my own Mac.

```text
CLIENT
curl
  ↓
HTTP request
  ↓
SERVER
Python HTTP Server
  ↓
HTTP response
  ↓
CLIENT
```

---

## What is `127.0.0.1`?

`127.0.0.1` refers to my own computer.

It is commonly called the loopback address.

For this lesson, I can think of:

```text
127.0.0.1
    ↓
Which computer?

8000
 ↓
Which service/port?
```

---

## What is a Port?

A port helps identify which service on a computer should receive a request.

For example:

```text
127.0.0.1:8000
127.0.0.1:8001
```

Both addresses point to my computer, but the ports can represent different running services.

A beginner mental model:

```text
IP address = building
Port       = door
```

---

## What Does `LISTEN` Mean?

I used:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

and saw a Python process listening on port 8000.

`LISTEN` means that a process is waiting for incoming connections.

This helped me confirm whether a service was actually running before blaming another part of the system.

---

# 2. Understanding System Layers

I learned that a **layer** is simply one part of a system with a particular job.

For my current exercise:

```text
Client
curl
  ↓
Network / Address + Port
127.0.0.1:8000
  ↓
Server
Python HTTP Server
  ↓
Resource
attendance-policy.txt
```

The important troubleshooting question became:

> **How far did the request get?**

This helped me distinguish between a resource problem and a server problem.

---

# 3. HTTP Results I Observed

## `200 OK`

When I requested the existing attendance policy while the server was running, I got:

```text
200 OK
```

This meant:

```text
Reached server      ✅
Found resource      ✅
Request succeeded   ✅
```

---

## `404 File Not Found`

When I requested a missing file, I got:

```text
404 File Not Found
```

This taught me something important:

> A `404` does not mean the server is down.

The server had to be reachable in order to send the `404`.

It means:

```text
Reached server      ✅
Server responded    ✅
Resource missing    ❌
```

Possible causes include:

- wrong filename
- wrong URL
- wrong directory
- missing file
- application routing problem

---

## Connection Refused

When nothing was listening on a port, I received a connection-refused error.

This meant:

```text
Reached HTTP server   ❌
HTTP status received  ❌
```

This is different from a `404`.

In this situation I should investigate:

- Is the server running?
- Is the correct port being used?
- Is a process listening on that port?
- Is the address correct?

---

# 4. Port Conflict Troubleshooting

I tried starting a second Python HTTP server on a port that was already in use.

I received:

```text
OSError: [Errno 48] Address already in use
```

I learned that two processes generally cannot listen on the same IP address and port combination at the same time.

Using:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

helped me identify which Python process already owned the port.

This showed me why checking the actual running process is better than guessing.

---

# 5. Python Health Checker

I created `endpoint_check.py` to automate the same troubleshooting I was doing manually with `curl`.

The endpoint list:

```python
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
```

---

## Lists and Dictionaries

I reviewed the difference between Python lists and dictionaries.

```text
[] = list
{} = dictionary
```

`endpoints` is a list.

Each item inside `endpoints` is a dictionary.

For example:

```python
endpoints[0]["url"]
```

means:

```text
Get the first item in the list
        ↓
Get the value stored under "url"
```

I also learned that a Python dictionary is not the same thing as JSON, even though they often look similar.

---

# 6. Using `urlopen()`

I learned how Python can send a request using:

```python
from urllib.request import urlopen
```

Then:

```python
response = urlopen(url, timeout=3)
```

means:

1. Attempt to open the URL.
2. Wait no longer than the specified timeout for the relevant network operation.
3. Save the returned HTTP response object in `response`.

This is similar to using `curl`, except Python can inspect the response and make decisions automatically.

---

# 7. HTTP Status in Python

The Python documentation showed that the modern way to access the status code is:

```python
response.status
```

For example:

```text
200
```

This connects directly to what I previously saw manually with `curl`.

---

# 8. Error Handling With `try` and `except`

I learned that network requests do not always succeed.

Instead of allowing one failed request to crash the entire program, I used:

```python
try:
    ...
except:
    ...
```

The basic idea is:

```text
TRY
↓
Attempt the network request

IF AN ERROR HAPPENS
↓
EXCEPT
↓
Handle the error instead of crashing
```

---

## `HTTPError`

I used:

```python
except HTTPError as error:
```

An `HTTPError` means the HTTP server responded, but returned an error status.

Example:

```text
404 File Not Found
```

Useful values include:

```python
error.code
error.reason
```

For a 404:

```text
error.code   → 404
error.reason → File not found
```

---

## `URLError`

I used:

```python
except URLError as error:
```

For this exercise, `URLError` handled the case where the service could not be reached successfully.

For example:

```text
Connection refused
```

Useful information:

```python
error.reason
```

---

# 9. Why `HTTPError` Comes Before `URLError`

The documentation explained that `HTTPError` is a subclass of `URLError`.

That means `HTTPError` is a more specific kind of URL-related error.

So my handlers are ordered:

```python
except HTTPError as error:
    ...

except URLError as error:
    ...
```

The more specific error is handled first.

---

# 10. Designing a Consistent Result Dictionary

I designed every health-check result to use the same fields:

```python
{
    "url": ...,
    "reachable": ...,
    "status": ...,
    "state": ...,
    "error": ...
}
```

These fields were not required by the Python documentation.

I chose them because they answer useful troubleshooting questions.

## `url`

```text
What did I check?
```

## `reachable`

```text
Did I successfully reach an HTTP server?
```

## `status`

```text
What HTTP status code did I receive?
```

Examples:

```text
200
404
```

## `state`

A label that my program uses to classify the result.

Examples:

```text
healthy
http_error
url_error
```

## `error`

A readable description of the error when one exists.

---

# 11. Why I Used `None`

For a healthy request:

```python
"error": None
```

means:

> There is no error value.

For an unreachable service:

```python
"status": None
```

means:

> No HTTP status code was received.

This is important because an unreachable service never returned something like `200` or `404`.

`None` is a real Python value that represents the absence of a value.

It is different from:

```python
"None"
```

because `"None"` is simply a string containing text.

---

# 12. Final `check_endpoint()` Function

```python
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
```

---

# 13. Looping Through All Endpoints

I created an empty list:

```python
results = []
```

Then checked every endpoint:

```python
for endpoint in endpoints:
    result = check_endpoint(endpoint["url"])
    results.append(result)
    print(result)
```

This taught me how to combine:

- lists
- dictionaries
- loops
- functions
- HTTP requests
- error handling

into one useful program.

---

# 14. Final Test Results

My final test produced three different states.

## Primary Policy

```text
reachable: True
status: 200
state: healthy
error: None
```

Meaning:

```text
Server reachable    ✅
Resource exists     ✅
Request healthy     ✅
```

## Missing Policy

```text
reachable: True
status: 404
state: http_error
error: File not found
```

Meaning:

```text
Server reachable    ✅
Resource exists     ❌
```

## Alternate Policy

```text
reachable: False
status: None
state: url_error
error: Connection refused
```

Meaning:

```text
HTTP service reachable   ❌
HTTP status received     ❌
```

This was the clearest demonstration of the main Day 3 troubleshooting lesson.

---

# 15. FDE Troubleshooting Mental Model

My biggest takeaway is:

> **Do not guess which part of the system is broken. Use evidence to determine how far the request traveled.**

```text
200
↓
Reached server
↓
Resource found
↓
Healthy
```

```text
404
↓
Reached server
↓
Server responded
↓
Resource problem
```

```text
Connection refused
↓
No HTTP response
↓
Investigate server/process/port/network
```

---

# 16. How This Applies to Forward Deployed Engineering

A customer may say:

> “The AI application is broken.”

But a real production system could look like:

```text
Student
  ↓
Browser
  ↓
Network
  ↓
Cloud
  ↓
FastAPI
  ↓
RAG
  ↓
Database / Vector Store
  ↓
LLM
  ↓
Response
```

The problem could exist anywhere in that chain.

Today reinforced that an FDE should ask:

> **What evidence do I have, and how far did the request get?**

I should not immediately blame the LLM.

A connection failure could occur before the AI system is ever reached.

A `404` may indicate a routing or resource problem.

A `200` may confirm that infrastructure is healthy even if the AI response quality is poor.

---

# 17. Day 3 Reflection

Today was useful because I realized that I had been using several networking terms and commands without fully understanding what they meant.

At first, terms such as `curl`, ports, layers, HTTP responses, and `LISTEN` were being used faster than I could connect them together.

Once I slowed down and understood each concept, the exercises became much easier to reason about.

One of the most important realizations was that `curl` is simply a client that sends a request to a service and shows the response.

That made the transition to Python easier because I could see that:

```text
curl
↓
send request

and

urlopen()
↓
send request
```

are solving a similar problem in different ways.

Another major learning moment was understanding that a `404` and a connection failure are fundamentally different.

Before this exercise, it would have been easy to group both under:

> “The server isn't working.”

Now I understand that a `404` actually proves that the server responded.

That means the troubleshooting path should focus more on the requested resource, path, or application configuration.

A connection refusal provides very different evidence because no HTTP response was received.

The Python portion also helped reinforce basic programming concepts that will matter later in my FDE journey.

I practiced:

- lists
- dictionaries
- nested data
- loops
- functions
- return values
- `None`
- exception handling
- reading official documentation
- debugging syntax errors
- translating documentation into working code

I also learned that documentation does not always directly tell me how to design my program.

For example, Python gave me values such as:

```text
response.status
error.code
error.reason
```

but I decided to organize those into my own consistent structure:

```text
url
reachable
status
state
error
```

That is an important engineering lesson.

Libraries provide tools and data, but engineers still have to decide how the application should represent and use that information.

I also made syntax mistakes during the exercise, such as missing commas inside a dictionary.

Instead of treating that as failure, I used the Python error message and line number to find the issue.

After correcting those errors, the final script successfully distinguished:

```text
healthy endpoint
missing resource
unreachable service
```

That felt like a meaningful step forward because I was no longer only running commands manually.

I created a small program that can make a troubleshooting decision based on evidence.

---

# 18. Day 3 FDE Takeaways

1. `curl` is a client used to send requests and inspect responses.
2. A port identifies which service on a computer should receive a connection.
3. `LISTEN` means a process is waiting for incoming connections.
4. `200` means the request succeeded.
5. `404` means the server responded but the requested resource was not found.
6. Connection refused means no service accepted the connection at that address and port.
7. `urlopen()` allows Python to send a request programmatically.
8. `response.status` gives the successful HTTP response status.
9. `HTTPError` handles HTTP error responses such as `404`.
10. `URLError` can represent problems opening/reaching a URL.
11. `None` represents the absence of a value.
12. Consistent dictionary fields make program results easier to process.
13. One bad endpoint should not crash the entire health checker.
14. An FDE should diagnose with evidence before deciding which system layer is broken.
15. “How far did the request get?” is a strong troubleshooting question.

---

# 19. Day 3 Completion Checkpoint

## Completed

- [x] Understand basic client/server communication
- [x] Understand what `curl` does
- [x] Understand basic ports
- [x] Use `lsof` to identify a listening process
- [x] Observe `200 OK`
- [x] Observe `404 File Not Found`
- [x] Observe a connection-refused error
- [x] Understand the difference between HTTP failure and connection failure
- [x] Use `urlopen()`
- [x] Use a three-second timeout
- [x] Read an HTTP status with `response.status`
- [x] Handle `HTTPError`
- [x] Handle `URLError`
- [x] Use consistent result dictionaries
- [x] Loop through multiple endpoints
- [x] Build and successfully run `endpoint_check.py`

## Next Step

The next step is to move from Python's simple static HTTP server toward a real application server.

A logical next milestone for the **B2D Cloud AI Knowledge Assistant** is to build a small FastAPI service with endpoints such as:

```text
GET /health
GET /documents
```

This will connect today's networking and HTTP knowledge to API development and eventually to RAG, cloud deployment, observability, and production troubleshooting.
