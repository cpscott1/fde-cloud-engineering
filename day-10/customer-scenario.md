# Day 10 Customer Scenario: Empty Knowledge Base

**Situation:** A rural Oklahoma school district has deployed the B2D Knowledge Assistant. The IT administrator reports that `/health` works, but `/documents` returns an empty list.

---

## 1. Diagnosis

**Why can `/health` return `200 OK` even when the knowledge documents are missing?**

`/health` only proves the web server is running. In `app.py` it returns `{"status": "ok"}` and never touches the knowledge folder. "Healthy" means FastAPI and uvicorn started, not that the assistant has anything to answer from.

`/documents` comes back empty without an error because `load_documents()` runs `knowledge_dir.glob("*.txt")`. If that folder is missing or empty, `glob` simply finds nothing. The result is `[]`, with no exception and no 500. The app fails silently.

Possible causes in this codebase:

- `/app/knowledge` never made it into the image (build problem, see #3).
- `B2D_KNOWLEDGE_DIR` is set on the district's server and points to a path that does not exist, overriding the default.
- A volume is mounted over `/app/knowledge` (for example `-v /srv/b2d/knowledge:/app/knowledge` against an empty host folder), hiding the files baked into the image.
- The files are not `.txt`. A `handbook.pdf`, `policy.docx`, or `NOTES.TXT` will not match `*.txt`.

---

## 2. Investigation

**Which Docker commands would you use to inspect the container and its knowledge directory?**

```bash
# Is it running, and which image/tag is it on?
docker ps
docker inspect <container> --format '{{.Config.Image}}'

# What is actually in the knowledge folder inside the running container?
docker exec <container> ls -la /app/knowledge

# Is the env var overriding the path?
docker exec <container> printenv B2D_KNOWLEDGE_DIR
docker inspect <container> --format '{{json .Config.Env}}'

# Is a volume mounted over /app/knowledge?
docker inspect <container> --format '{{json .Mounts}}'

# Does the IMAGE itself contain the files? (separates build problem from run problem)
docker run --rm <image> ls -la /app/knowledge

# Did the COPY knowledge/ layer add anything?
docker history <image>

# App logs and the endpoints themselves
docker logs <container>
curl http://localhost:8000/health
curl http://localhost:8000/documents
```

**Key comparison:** `docker run --rm <image> ls` vs `docker exec <container> ls`.

- Image has files, container does not: **runtime problem** (volume or env var).
- Image is also empty: **build problem**.

---

## 3. Resolution

**If `/app/knowledge` is empty, what would you check in the Dockerfile and build process?**

- **Build context.** `COPY` paths are relative to the build context, which is set by the final argument to `docker build`, not necessarily the directory containing the Dockerfile. Our current command works because we run `docker build -t b2d-assistant .` from inside `day-10`, so the context `.` contains `knowledge/`. Running `docker build -f day-10/Dockerfile .` from the repo root would make the repo root the context, and `COPY knowledge/` would not find the folder.
- **`.dockerignore`.** Currently fine (only excludes `.venv`, `__pycache__`, `.git`, `.env`, etc.). Make sure `knowledge/` or `*.txt` never gets added.
- **Source files exist.** Run `ls day-10/knowledge` on the build machine. If the district cloned from Git, confirm the `.txt` files were committed and are not in `.gitignore`.
- **File types.** Only `.txt` files load. Convert or rename anything else.
- **Stale image or cache.** Rebuild with `docker build --no-cache -t b2d-assistant:<new-tag> .` and confirm the running container uses the new tag.
- **Verify the fix:** `docker exec <container> ls /app/knowledge` and `curl /documents` should show `attendance-policy.txt`, `career-guide.txt`, and `student-handbook.txt`.

**Prevention (proposed):** Proposed adding a `/ready` endpoint that returns `503` when zero documents are loaded. `/health` would stay a simple "is the server on" check (liveness), and `/ready` would answer "can it actually do its job" (readiness). This is not yet implemented or verified in `app.py`. Implementing it would also require building and testing a new image before it could be deployed.

---

## 4. Customer Communication

**How would you explain the issue and verification steps to a school IT administrator without a programming background?**

> Hi [Name], thanks for the clear report, that made this quick to track down.
>
> Here's what happened: the assistant has two parts, the program itself and the folder of school documents it reads from (handbook, attendance policy, career guide). The health check only confirms the program is switched on. It doesn't look inside the documents folder. So the program was running fine, but its documents folder was empty, which is why the document list came back blank.
>
> Think of it like a librarian who showed up to work, but the bookshelves never got delivered.
>
> What we're doing: checking both the documents packaged with the assistant and the server's configuration settings to identify the cause before applying a fix.
>
> How you can confirm it's fixed:
> 1. Open http://[server]:8000/documents in a browser. You should see three file names listed.
> 2. Ask the assistant something like "What is the attendance policy?" and confirm it answers using the attendance document.
>
> I'll follow up once we've confirmed the cause and the fix is in place.
