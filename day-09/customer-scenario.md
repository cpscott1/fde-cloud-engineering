# Day 9 Customer Scenario — Docker Connectivity Troubleshooting

## Scenario

A school district IT engineer says:

> “The container is running, but I can’t open the application in my browser.”

As the Forward Deployed Engineer, I should not immediately assume the application code is broken.

I should first verify the container, networking, and logs.

## Step 1 — Check whether the container is running

Run:

```bash
docker ps
```

This tells me:

- whether the container is currently running,
- which image it is using,
- the container name,
- and which ports are published.

If the expected container does not appear, the problem may be that the container stopped or never started successfully.

## Step 2 — Test the published port

Run:

```bash
curl -i http://127.0.0.1:8080
```

This tests whether the service can be reached through the port published on my machine.

During the Day 9 exercise, this returned:

```text
HTTP/1.1 200 OK
```

That proved traffic successfully traveled from:

```text
my Mac on port 8080
→ Docker
→ container port 80
→ nginx
```

## Step 3 — Inspect the container logs

Run:

```bash
docker logs b2d-port-test
```

This lets me see:

- application startup information,
- errors,
- and incoming requests.

During the exercise, the nginx logs showed the request from `curl` and a `200` response.

## Troubleshooting Pattern

My basic Docker troubleshooting flow is:

```text
docker ps
→ Is the container actually running?

curl
→ Can I reach the service?

docker logs
→ What is the application reporting?
```

I can think of this as:

```text
state
→ connectivity
→ logs
```

## Port Mapping

The container was started using:

```text
8080:80
```

This means:

```text
8080 = port on my Mac
80   = port inside the container
```

Docker forwards traffic from the host port to the container port.

If the wrong host port is used in the browser or `curl` command, the application may appear unavailable even though the container itself is healthy.

## FDE Lesson

A customer saying “the application does not work” does not automatically mean there is a code bug.

The issue could instead involve:

- container state,
- port publishing,
- networking,
- application startup,
- or runtime configuration.

Before modifying application code, I should collect evidence from the running system.

## Security and Privacy Note

When troubleshooting an education application, logs should contain only the information necessary to diagnose the problem.

I should avoid unnecessarily logging:

- student names,
- private student records,
- credentials,
- sensitive questions,
- or full confidential document contents.

## Day 9 Takeaway

A useful FDE troubleshooting process is:

```text
verify the runtime
→ verify connectivity
→ inspect logs
→ then investigate application code if needed
```

This helps me avoid changing working code when the actual problem is in the runtime or network configuration.