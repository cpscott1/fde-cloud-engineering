# Day 9 Reflection

## Where I am
Day 9 is about packaging the B2D Knowledge Assistant with Docker. My starting checkpoint
was `docker --version` returning `command not found`, so Docker isn't installed yet.
I carried the Day 8 app forward unchanged, so the container work starts from the
version that passed 4 of 4.

## What I practiced in Python
- f-strings to build a port mapping (`8000:80`) and a container description
- a dictionary for a container's config, plus adding a new key (`environment`)
- a function with a parameter that returns a string instead of printing it
- a list of dictionaries for readiness checks, looped with a counter
- collecting failed checks into a list
- readiness logic: ready only when every check passes
- an early return: `all_checks_passed()` returns False at the first failed check

## What is practice vs. verified
The readiness checks in `python_refresher.py` use values I typed in. They show how I'd
decide "ready to build," but they don't prove Docker works. Still to verify with real
output: Docker CLI, Docker engine, the hello-world container, and a published HTTP port.

## Why this matters for an FDE
Same lesson as Day 8: don't call it ready because the code looks right. Check what's
actually installed and running, and record the evidence. A readiness checklist with
pass/fail and a list of what failed is something a district IT person could follow.

## Next step
Install Docker Desktop, run the four checks, record the real output in `docker-notes.md`,
then write the first Dockerfile for the B2D app.

## Docker Fundamentals Checkpoint

### Concepts I learned

**1. What is the difference between a Docker image and a Docker container?**

My answer: An image is the packaged, read-only blueprint. It holds the app code, the
dependencies, and the instructions for how to start it. A container is a running instance
of that image. I build an image once and can start many containers from it, and each
container gets its own writable layer that goes away when the container is removed.
Think of the image as the recipe and the container as the meal made from it.

**2. What does the port mapping `8000:80` mean?**

My answer: The format is `host:container`. Traffic that hits port 8000 on my machine
gets forwarded to port 80 inside the container. So if the app listens on port 80 inside
the container, I open `http://localhost:8000` in my browser to reach it. Without a port
mapping, the app runs but nothing outside the container can reach it.

**3. What does the `--rm` option do when running a container?**

My answer: `--rm` tells Docker to delete the container automatically as soon as it stops.
It's useful for quick tests like `docker run --rm hello-world` so stopped containers don't
pile up. The image stays; only that container instance is cleaned up.

**4. Why is a real Docker test more reliable than setting `docker_engine = True` in Python?**

My answer: `docker_engine = True` is just a value I typed. It says what I expect, not what
is true. A real test like `docker version` or `docker run --rm hello-world` asks the actual
system and returns real output, so it would catch problems my variable can't: Docker not
installed, the engine not running, a permissions issue, or a blocked network pull. The
terminal output is evidence I can paste into my notes and show someone else.

### Actual Docker verification

- Docker CLI: Pending verification (run `docker --version`)
- Docker engine: Pending verification (run `docker version` or `docker info` and confirm a Server section appears)
- Hello-world container: Pending verification (run `docker run --rm hello-world`)
- Published HTTP port test: Pending verification (run `docker run --rm -d -p 8000:80 nginx`, open `http://localhost:8000`, then stop the container)

### Day 9 completion status

Python refresher: Completed based on the results I shared.

Docker verification: Pending confirmation from real terminal output.

Customer scenario: Pending confirmation.

### Next engineering milestone

Build the first Docker image containing the B2D Knowledge Assistant's FastAPI application, retrieval logic, and knowledge documents.