# Day 8 Deployment Readiness

## Verified environment

- Virtual environment: `.venv`
- Python version: `3.14.7`
- Dependencies recorded in `requirements.txt`
- `python3 -m pip check` result: `No broken requirements found.`

## Verified retrieval

Day 8 evaluation result:

- Passed: `4`
- Total: `4`
- Accuracy: `100.0%`

The known Day 7 failure was:

`Are cellphones allowed?`

Expected source:

`student-handbook.txt`

Actual Day 7 result:

`None`

The failure happened because the retrieval system relied on exact word overlap. The question used `cellphones`, while the handbook used `phones`.

Day 8 added word normalization so these words are treated as the same concept:

- `cellphone` → `phone`
- `cellphones` → `phone`
- `phones` → `phone`

After the change, the evaluation improved from:

`3/4 — 75%`

to:

`4/4 — 100%`

This does not mean the retrieval system is perfect. It means all four current evaluation cases pass.

## Verified FastAPI application

The FastAPI server starts with:

`python3 -m uvicorn app:app --host 0.0.0.0 --port 8000`

The health endpoint returned:

`{"status":"ok"}`

The documents endpoint returned:

- `attendance-policy.txt`
- `student-handbook.txt`
- `career-guide.txt`

The live `/ask` endpoint was tested with:

`Are cellphones allowed?`

The verified result was:

- Source: `student-handbook.txt`
- Score: `1`

## Runtime troubleshooting incident

The retrieval evaluation passed, but the live FastAPI endpoint initially continued returning:

- Source: `None`
- Score: `0`

This showed that the source code on disk was correct, but the running application was not behaving like the current code.

I checked which processes were listening on port 8000 with:

`lsof -nP -iTCP:8000 -sTCP:LISTEN`

Multiple Python processes were listening on the same port.

After stopping the stale processes and starting one clean Day 8 Uvicorn process, the live API returned the correct result.

## FDE troubleshooting lesson

This incident showed that a passing local test does not guarantee that the running application is using the same code.

When tests pass but the live service behaves differently, I should investigate:

1. Which process is actually running.
2. Which port the process is listening on.
3. Whether an older application process is still active.
4. Which environment and Python interpreter are being used.
5. Whether the application was restarted after a code change.
6. What the runtime logs show.

This helps separate a code problem from a runtime or deployment problem.

## Why this matters for cloud engineering

Manually checking processes with `lsof` is useful for understanding what is happening locally, but it is not the long-term production model.

A production application should move toward:

- a reproducible runtime,
- one clearly owned application process,
- containerization,
- automated health checks,
- controlled restarts,
- centralized logs,
- and eventually orchestration or managed cloud infrastructure.

The stale-process problem is one reason containerization matters.

Instead of relying on whatever processes happen to be running on a developer machine, a container defines a repeatable application runtime.

## Governance and security note

The retrieval logs currently record:

- selected source,
- retrieval score.

They do not need to record:

- student