# Day 12 — Docker Security Evidence

## Objective

Run the B2D Knowledge Assistant as a non-root
Linux user without breaking application functionality.

## Docker Image

Image: b2d-knowledge-assistant:day12

Build result: Successful

## Non-Root User Verification

Configured Docker image user: appuser

Observed container user:
- UID: 10001 (appuser)
- GID: 10001 (appgroup)

Result: PASS

## Application Verification

| Test | Observed Result | Result |
|---|---|---|
| GET /health | HTTP 200, status ok | PASS |
| GET /ready | HTTP 200, ready, 3 documents | PASS |

## Security Takeaway

The application successfully runs as a non-root
user while maintaining access to its knowledge documents.

Running as a non-root user reduces unnecessary
privileges but does not eliminate all security risks.

## Automatic Docker Health Check Verification

### Healthy Configuration

Container: b2d-day12-ok

- Knowledge directory: /app/knowledge
- Docker health status: healthy
- Result: PASS

### Incorrect Knowledge Directory

Container: b2d-day12-bad

- Environment variable: B2D_KNOWLEDGE_DIR=/tmp/b2d-empty
- GET /ready: HTTP 503
- Readiness status: not_ready
- Document count: 0
- Docker health status: unhealthy
- Result: PASS - expected failure detected

### Key Finding

Both containers continued running, but Docker reported
different health states.

This demonstrates that a running container is not
necessarily ready to serve users.

The unhealthy test passed because Docker correctly
detected the missing knowledge documents.

An unhealthy production container would require
investigation and corrective action.