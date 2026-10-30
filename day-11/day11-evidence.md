# Day 11 Readiness Evidence

## Normal Configuration

| Test | Observed Result | Matches Expected |
|---|---|---|
| GET /health | HTTP 200, status ok | Yes |
| GET /ready | HTTP 200, ready, 3 documents | Yes |

## Incorrect Knowledge Directory

Configured value: B2D_KNOWLEDGE_DIR=/tmp/b2d-empty

| Test | Observed Result | Matches Expected |
|---|---|---|
| GET /health | HTTP 200, status ok | Yes |
| GET /ready | HTTP 503, not_ready, 0 documents | Yes - expected failure detected |

Important: HTTP 503 indicates the application is not ready. The test
passed because the readiness endpoint correctly detected the missing
knowledge documents. A production deployment should not be considered
healthy while `/ready` returns 503.

## Container Cleanup

- b2d-ready stopped successfully.
- b2d-not-ready stopped successfully.
- docker ps confirmed no running test container.
- docker ps -a confirmed b2d-not-ready was removed.

## FDE Takeaway

A running application is not necessarily ready to serve users.
A readiness endpoint can detect missing dependencies even when
the web server continues responding normally.
