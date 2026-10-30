# Day 12 Reflection

## What I Built

I made two upgrades to the B2D Knowledge Assistant. First, I locked it down so the container runs as a non-root user called `appuser` instead of root. Second, I added a Docker HEALTHCHECK that hits the `/ready` endpoint every 10 seconds, so Docker can tell me whether the app can actually find its knowledge documents, not just whether the process is up.

## What I Learned About Non-Root Containers

UID `10001` is the user ID I gave `appuser` (and GID `10001` for `appgroup`). Linux cares about the number, not the name, and picking a high number makes it less likely to collide with real users or system accounts on the host or a mounted filesystem, though it doesn't guarantee it. Running as non-root is safer because if someone ever breaks into the app, they only get the limited permissions of that user instead of full root inside the container. It doesn't make the app bulletproof, but it shrinks the blast radius.

## What I Learned About Docker Health Checks

A running container just means the process hasn't crashed. A healthy container means the app is passing its own check and is actually ready to serve people. My tests proved it: `b2d-day12-ok` and `b2d-day12-bad` were both running, but the bad one pointed `B2D_KNOWLEDGE_DIR` at an empty folder, so `/ready` returned a 503 with zero documents and Docker flagged it as unhealthy. That was the expected failure, and it showed me "up" and "working" are two different things.

## What I Learned About Python

`elif` lets me check one condition after another and stop at the first match, which is how my `explain_health()` function turns "starting," "healthy," or "unhealthy" into a plain-English message, with `else` catching anything unknown. A consecutive-failure counter adds one every time a probe fails and resets to zero on a success, which is the same idea Docker uses with `--retries=3`. Assertions are quick self-checks: if the result doesn't match what I expect, the script stops and shows my error message, so I know right away something broke.

## Customer Troubleshooting Lessons

Before restarting anything, I'd gather evidence. I'd run `docker inspect` to check the `B2D_KNOWLEDGE_DIR` variable and any mounts, `docker exec` in to see what files are really in the knowledge folder and whether UID 10001 can read them, confirm they're `.txt` files, and check `docker logs` for errors. I'd also ask the district what changed recently, because a restart with the same bad config just brings back the same problem.

## Biggest Challenge

The hardest part for me was separating "running" from "ready." At first it felt like if the container was up, the app was fine. Seeing two containers both running with different health states, and tracing that back to `/ready` returning a 503, is what finally made it click.

## Next Step

Docker Compose would let me put the whole setup in one `docker-compose.yml` file: the image, port, environment variables, knowledge volume, and health check. Instead of typing long `docker run` commands for each district, I could run `docker compose up` and get the same configuration every time. That makes deployments more repeatable and makes it easier to spot when a district's config is different from what it should be.
