# Day 11 Customer Scenario: Assistant Online, Policies Missing

**Situation:** A rural Oklahoma school district reports that its B2D Knowledge Assistant is online but can't pull up any of its school policies.

**What I verified during this incident simulation:**

```
GET /health → 200 OK
GET /ready  → 503 Service Unavailable
document_count → 0
B2D_KNOWLEDGE_DIR → /tmp/b2d-empty
```

The container was published at `127.0.0.1:8002`, so every command below uses that address.

---

## 1. Diagnosis

**Why does `/health` work while `/ready` fails?**

They're answering two different questions. `/health` only asks "is the server up?" In `app.py` it returns `{"status": "ok"}` and never touches the knowledge folder, so as long as FastAPI and uvicorn started, it passes.

`/ready` asks "does the assistant actually have something to answer from?" It calls `load_documents()`, counts what comes back, and if the count is 0 it returns a 503 with `{"status": "not_ready", "document_count": 0}`.

So the server is up, but the assistant isn't ready to do its job. On Day 10 I identified that I needed a readiness endpoint, because this same problem only showed up as an empty `/documents` list somebody had to dig into. On Day 11 I implemented `/ready`, and this incident is exactly what it's for. The app tells on itself with a clear failure instead of failing silently.

---

## 2. Root Cause

**How did the `B2D_KNOWLEDGE_DIR` setting affect document retrieval?**

In `retrieval.py`, the app decides where to look for documents when it starts:

```python
DEFAULT_KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"
configured_directory = os.getenv("B2D_KNOWLEDGE_DIR")
knowledge_dir = Path(configured_directory) if configured_directory else DEFAULT_KNOWLEDGE_DIR
```

If `B2D_KNOWLEDGE_DIR` is set, it wins over the default. In this container it was set to `/tmp/b2d-empty`, so the app skipped `/app/knowledge` (where the Dockerfile copies the policy files) and looked in a folder with no `.txt` files.

`knowledge_dir.glob("*.txt")` found nothing, `load_documents()` returned `[]`, and `/ready` reported `document_count: 0`. Based on the code, the other document endpoints would come up empty for the same reason:

- `/documents` → `{"documents": []}`
- `/ask` → `source: null`, `context: null`, `score: 0`

The Dockerfile copies `knowledge/` into `/app/knowledge`, so the policy files should still be in the image. The app was pointed at the wrong folder. That's my working conclusion; the file inspection in step 3 is how I'd confirm it.

One more detail that matters for the fix: the path is read once when the app starts, and a container's environment variables are locked in when the container is created. So fixing it means starting a new container with the right setting, not just restarting the app.

---

## 3. Investigation

**Which Docker commands helped establish the problem?**

**Completed during this simulation:**

```bash
# Server up?
curl -i http://127.0.0.1:8002/health      # 200 OK

# Assistant ready?
curl -i http://127.0.0.1:8002/ready       # 503, document_count: 0

# What is the knowledge path set to inside the container?
docker exec <container> printenv B2D_KNOWLEDGE_DIR    # /tmp/b2d-empty
```

Those three results establish the problem: the server is running, the app has zero documents, and an environment variable is overriding the default knowledge path.

**Next investigation steps (not yet performed):**

```bash
# Confirm which container and image/tag are running
docker ps

# Full environment and any volume mounts
docker inspect <container> --format '{{json .Config.Env}}'
docker inspect <container> --format '{{json .Mounts}}'

# What's in the configured folder vs. the default folder?
docker exec <container> ls -la /tmp/b2d-empty
docker exec <container> ls -la /app/knowledge

# Does the image itself have the files? (separates a build problem from a runtime problem)
docker run --rm <image> ls -la /app/knowledge

# Retrieval log lines (source=None score=0 would confirm nothing is being found)
docker logs <container>
```

What I'd expect if my diagnosis is right: `/tmp/b2d-empty` has no `.txt` files, and `/app/knowledge` still has `attendance-policy.txt`, `career-guide.txt`, and `student-handbook.txt`. That would make it a **runtime configuration problem**, not a build problem.

---

## 4. Resolution

**What configuration change would restore the correct knowledge directory?**

Start a new container without the bad override, or with it set to the right path. My test container was started with `--rm`, so stopping it also removes it. No separate `docker rm` needed. (Without `--rm`, I'd have to run `docker rm <container>` after stopping it.)

```bash
# Stop the misconfigured container (--rm removes it automatically)
docker stop <container>

# Option A: don't set the variable, so the app falls back to /app/knowledge
docker run --rm -d --name b2d-assistant -p 127.0.0.1:8002:8000 <image>

# Option B: set it explicitly to the correct path
docker run --rm -d --name b2d-assistant -p 127.0.0.1:8002:8000 \
  -e B2D_KNOWLEDGE_DIR=/app/knowledge \
  <image>
```

I'd lean toward Option B for the district. Being explicit makes the setting easy to see in `docker inspect`, so the next person troubleshooting doesn't have to guess.

If the district runs it with Docker Compose or an `.env` file, the value needs fixing there too. Otherwise the bad setting comes right back on the next redeploy.

**Preventing it next time:** document `B2D_KNOWLEDGE_DIR` in the deployment notes with the correct production value, and add a `/ready` check to whatever startup script or monitoring the district uses, so a 503 gets caught on day one instead of when a staff member asks a question.

---

## 5. Verification

**Which API responses would demonstrate that the issue is resolved?**

These checks haven't been run yet. They're what I'd run after the fix is applied:

| Check | Command | Expected result once fixed |
|---|---|---|
| Correct path | `docker exec <container> printenv B2D_KNOWLEDGE_DIR` | `/app/knowledge` (or nothing, if using the default) |
| Server up | `curl -i http://127.0.0.1:8002/health` | `200 OK`, `{"status": "ok"}` |
| Assistant ready | `curl -i http://127.0.0.1:8002/ready` | `200 OK`, `{"status": "ready", "document_count": 3}` |
| Documents loaded | `curl http://127.0.0.1:8002/documents` | `attendance-policy.txt`, `career-guide.txt`, `student-handbook.txt` |
| Retrieval works | `curl -X POST http://127.0.0.1:8002/ask -H "Content-Type: application/json" -d '{"question": "What is the attendance policy?"}'` | `source: "attendance-policy.txt"` with a score above 0 |

The `/ready` result is the headline: 503 to 200 and `document_count` 0 to 3 is the before and after I'd show the customer. The `/ask` check matters too, because `/ready` only proves documents loaded. It doesn't prove a real question finds the right policy.

I'd save the real output from each check in the incident ticket so the district has proof, not just my word.

---

## 6. Customer Communication

**Explaining it to a principal or district technology director:**

> "Good news first: from what we've found so far, your policies aren't lost, and the assistant itself isn't broken.
>
> Think of the assistant like a librarian. The librarian showed up to work and is at the front desk, which is why it looks online. But a setting is telling the librarian to pull answers from an empty shelf instead of the shelf where your handbook and policies are kept. So when anyone asks a question, there's nothing to pull from.
>
> Our next step is to point it back to the right shelf. Once that's done, we'll test it by asking real questions, like the attendance policy, to confirm it's finding the right information again, and we'll let you know as soon as that's confirmed.
>
> To keep this from happening again, we'll write down the correct setting for your team and add a check that warns us right away if the assistant ever can't see its documents, so we catch it before your staff do."

If they ask "how long were people getting no answers?", I'd give a straight answer based on the logs and when the setting changed, not a guess.
