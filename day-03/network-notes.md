# Day 3 — Network Notes

## Concepts I Learned During Troubleshooting

### What is `curl`?

`curl` is a command-line tool that sends a request to a service and shows me the response from that service.

The service can be running on my own computer or on another computer/server over a network.

For example:

```bash id="mp46oc"
curl http://127.0.0.1:8001/attendance-policy.txt
```

This means I am asking the service running at `127.0.0.1` on port `8001` for the resource `attendance-policy.txt`.

A simple way for me to remember it:

```text id="f5i1tg"
curl
 ↓
Send request
 ↓
Service
 ↓
Send response
 ↓
curl displays response
```

`curl` is the **client** in this example. The Python HTTP server is the **server**.

---

### What does `curl -i` mean?

The `-i` option tells `curl` to also display the HTTP response headers.

For example:

```bash id="4g6dpz"
curl -i http://127.0.0.1:8001/attendance-policy.txt
```

can return information such as:

```text id="ej9by7"
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.9.6
Content-type: text/plain
Content-Length: 172
```

This is useful when troubleshooting because I can see information about how the server responded instead of seeing only the requested content.

---

### Client vs. Server

A **client** asks another service for something.

A **server** listens for requests and sends responses.

In my Day 3 exercise:

```text id="n9mdx3"
CLIENT
curl
 ↓
request
 ↓
SERVER
Python HTTP Server
 ↓
response
 ↓
CLIENT
curl
```

The client and server can be on different computers, but they do not have to be.

During this exercise, both were running on my Mac.

---

### Understanding `127.0.0.1`

`127.0.0.1` refers to my own computer.

During this exercise, I used:

```text id="vjv2p7"
127.0.0.1:8001
```

I can currently think about this as:

```text id="q9yk3g"
127.0.0.1
    ↓
Which computer/address?

8001
 ↓
Which service/door?
```

The service was not somewhere else on the internet. My `curl` client and Python server were communicating locally on my Mac.

---

### What is a Port?

A port helps identify which service on a computer should receive a network request.

For example:

```text id="ce9bh6"
127.0.0.1:8000
127.0.0.1:8001
```

Both use the same computer/address, but they can point to different running services.

A simple mental model is:

```text id="2zhxtv"
IP address = building
Port       = door
```

This is not a perfect technical definition, but it helps me understand why multiple services can run on the same computer.

---

### What Does `LISTEN` Mean?

When I ran:

```bash id="bbttzx"
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

I saw:

```text id="k73h23"
Python  2391  ...  TCP 127.0.0.1:8000 (LISTEN)
```

`LISTEN` means the Python process is waiting for incoming connections on that address and port.

The PID identifies the specific running process.

For example:

```text id="ij2l2n"
Python process
PID 2391
     ↓
Listening on
     ↓
127.0.0.1:8000
```

---

### What Does "Layer" Mean?

A layer is simply one part of a larger system that has a particular responsibility.

For my current exercise, I can think about the system like this:

```text id="i02m3w"
Client
curl
 ↓
Network
127.0.0.1:8001
 ↓
Server
Python HTTP Server
 ↓
Resource
attendance-policy.txt
```

Each part has a different job.

The client sends the request.

The network allows the request to reach the destination.

The server receives the request and determines how to respond.

The resource is the thing being requested.

---

### What is a Resource?

A resource is the thing the client is requesting from the server.

In this request:

```bash id="72q46m"
curl http://127.0.0.1:8001/attendance-policy.txt
```

the resource is:

```text id="cml7s6"
attendance-policy.txt
```

The server has to determine whether that resource exists and whether it can return it.

---

### How Far Did My Request Get?

A useful troubleshooting question I learned is:

> **How far did my request get?**

Instead of immediately assuming I know what is broken, I can use the response as evidence.

For my current system:

```text id="2m5k5n"
curl
 ↓
Network
 ↓
Python Server
 ↓
Requested File
```

Different results tell me different things.

#### `200 OK`

```text id="gz9gz8"
curl
 ↓
Reached server ✓
 ↓
Server found resource ✓
 ↓
200 OK
```

The request succeeded.

#### `404 File Not Found`

```text id="v54ykh"
curl
 ↓
Reached server ✓
 ↓
Server responded ✓
 ↓
Requested resource wasn't found ✗
 ↓
404
```

A `404` is important because the server actually responded.

That means I should not immediately assume that the server is completely unreachable.

I should investigate things such as:

```text id="yzdumf"
Is the filename correct?
Is the URL/path correct?
Does the file exist?
Is the server serving the correct directory?
```

#### Connection Failure

If the server is stopped, I may receive a connection error instead of an HTTP response.

Conceptually:

```text id="dlapmh"
curl
 ↓
tries to connect
 ↓
127.0.0.1:8001
 ↓
No service listening
 ↓
Connection fails
```

This is different from a `404`.

With a `404`, I reached an HTTP server.

With a connection failure, I did not receive an HTTP response from the service.

---

## Listening Process

### Server Command

```bash id="7c77a5"
python3 -m http.server 8000 --bind 127.0.0.1 --directory knowledge
```

### HTTP Request

```bash id="bxlmn4"
curl -i http://127.0.0.1:8000/attendance-policy.txt
```

### Recorded Response

```text id="4ru6us"
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.9.6
Date: Sun, 27 Sep 2026 03:18:43 GMT
Content-type: text/plain
Content-Length: 172
Last-Modified: Sun, 27 Sep 2026 03:10:28 GMT

B2D Demonstration Attendance Policy

Students should arrive before class begins.
Absences must be reported to the school office.
This file contains demonstration data only.
```

## Listening Process Check

### Command

```bash id="sqfhhm"
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

### Recorded Output

```text id="icrflx"
COMMAND  PID   USER           FD  TYPE  NAME
Python   2391  cameronperry   4u  IPv4  TCP 127.0.0.1:8000 (LISTEN)
```

### Process Information

- Command: `python3 -m http.server 8000 --bind 127.0.0.1 --directory knowledge`
- Process name: `Python`
- PID: `2391`
- IP address: `127.0.0.1`
- Port: `8000`
- State: `LISTEN`

---

## Port Conflict

### Command Attempted

```bash id="cnxsd9"
python3 -m http.server 8000 \
  --bind 127.0.0.1 \
  --directory knowledge
```

### Recorded Error

```text id="a8zzgi"
OSError: [Errno 48] Address already in use
```

The second Python HTTP server could not start on port `8000` while the original server was still listening on `127.0.0.1:8000`.

### Reflection

1. What was already using port 8000?

**My Answer:**


2. Why couldn't the second process listen on that same address and port?

**My Answer:**


3. How did `lsof` help confirm the cause?

**My Answer:**


---

## Testing a Different Port

After the port `8000` conflict, I attempted to run another Python HTTP server using port `8001`.

### Command

```bash id="f1gq5k"
python3 -m http.server 8001 \
  --bind 127.0.0.1 \
  --directory knowledge
```

### Server Started

```text id="6dhvhm"
Serving HTTP on 127.0.0.1 port 8001 ...
```

This showed that the Python HTTP server could use port `8001` while another server was already using port `8000`.

---

## Port 8001 Initial Request

I tested the new server with:

```bash id="t3xks4"
curl -i http://127.0.0.1:8001/attendance-policy.txt
```

### Recorded Response

```text id="ydgkvt"
HTTP/1.0 404 File not found
Server: SimpleHTTP/0.6 Python/3.9.6
Date: Sun, 27 Sep 2026 03:34:40 GMT
Connection: close
Content-Type: text/html;charset=utf-8
Content-Length: 469
```

### Observation

The `404 File not found` response showed that the server on port `8001` was reachable, but it could not find `attendance-policy.txt` in the directory it was serving.

This was different from a connection failure because the HTTP server successfully sent a response.

---

## Troubleshooting Port 8001

When I attempted to restart the server on port `8001`, I received:

```text id="i8g3dc"
OSError: [Errno 48] Address already in use
```

I checked which process was listening:

```bash id="n8q1hv"
lsof -nP -iTCP:8001 -sTCP:LISTEN
```

### Recorded Output

```text id="dxy54h"
COMMAND  PID   USER           FD  TYPE  NAME
Python   2585  cameronperry   4u  IPv4  TCP 127.0.0.1:8001 (LISTEN)
```

This confirmed that Python process PID `2585` was still listening on port `8001`.

---

## Port 8001 Successful Retry

After stopping the previous process, I started the server from inside the correct `knowledge` directory:

```bash id="r64rjv"
python3 -m http.server 8001 --bind 127.0.0.1
```

The server logged:

```text id="jdkyja"
127.0.0.1 - - [26/Sep/2026 22:39:25] "GET /attendance-policy.txt HTTP/1.1" 200 -
```

This confirmed that the client reached the server and the server successfully found and returned the requested file.

---

## Troubleshooting Timeline

```text id="rqwyys"
Server running on port 8000
        ↓
Try another server on port 8000
        ↓
Address already in use
        ↓
Use port 8001
        ↓
Server starts
        ↓
Request file
        ↓
404 File not found
        ↓
Server is reachable
but resource isn't available
        ↓
Check process/directory
        ↓
Restart from correct directory
        ↓
Request file again
        ↓
200 OK
```

---

## Request Results

| Experiment | HTTP status or error | Did we reach a server? | What evidence supports my answer? |
|---|---|---|---|
| Existing file | `200 OK` | Yes | The Python server returned the requested file and logged a successful `GET` request. |
| Missing file | | | |
| Stopped server | | | |

---

## Python Checkpoint

1. What does `urlopen()` do?

**My Answer:**


2. Why did the program need exception handling?

**My Answer:**


3. How did the program distinguish an HTTP error from a connection error?

**My Answer:**


4. How could this become a health check for the B2D Cloud AI Knowledge Assistant?

**My Answer:**


5. What part of my program was most difficult?

**My Answer:**