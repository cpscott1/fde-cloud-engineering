# B2D Knowledge Assistant Readiness Runbook

## Purpose

This runbook helps a district IT administrator troubleshoot the B2D Knowledge Assistant when it is running but not answering questions correctly. It explains how to tell the difference between a server that is simply up and an assistant that is actually ready to serve answers from the district's knowledge documents. Use it when staff or students report empty, missing, or failed answers.

## Expected Healthy Behavior

When the assistant is working correctly, both checks pass and the knowledge documents are loaded:

```
GET /health → 200 OK
GET /ready  → 200 OK
status         → ready
document_count → 3
```

- `/health` confirms the web server process is running and responding.
- `/ready` confirms the assistant found and loaded its knowledge documents.
- `document_count` of 3 matches the three files in the knowledge folder: `attendance-policy.txt`, `career-guide.txt`, and `student-handbook.txt`.

## Signs of a Problem

The failure reproduced on Day 11 looked like this:

```
GET /health → 200 OK
GET /ready  → 503 Service Unavailable
status         → not_ready
document_count → 0
```

**What this means:** The server is up, but the assistant has no knowledge to answer from.

**Why a server can be running while the assistant isn't ready:** `/health` only checks that the web server process is alive and can respond to a request. It does not look at the knowledge documents at all. `/ready` goes one step further and tries to load the `.txt` files from the knowledge folder. If that folder is missing, empty, or the `B2D_KNOWLEDGE_DIR` setting points to the wrong location, the server keeps running normally but finds zero documents. In that state the assistant cannot answer questions, so `/ready` returns `503` to signal that it should not receive traffic yet.

**Symptoms users may report:**

- Questions return no source or an empty answer.
- `/documents` returns an empty list.
- The assistant appears online, but every answer fails.

## Investigation Commands

### 1. Check Running Containers

Command: `docker ps`

Purpose: Displays all currently running Docker containers.

Day 11 observation: The command returned only column headings,
confirming no containers were running.

If the expected application container is missing, investigate
whether it stopped, crashed, or was never started.

### 2. Review Application Logs

First run:

`docker ps -a`

Find the actual container name in the NAMES column.

Then run:

`docker logs ACTUAL_CONTAINER_NAME`

Purpose: Review application startup messages and errors.

Day 11 observation: The b2d-ready container showed
"Application startup complete" while it existed.

Important: b2d-assistant was only an example name.
The Day 11 test containers were automatically removed
after stopping because they used --rm.

### 3. Check the Knowledge Directory Setting

First, identify the actual running container:

`docker ps`

Then check its knowledge directory setting:

`docker exec ACTUAL_CONTAINER_NAME printenv B2D_KNOWLEDGE_DIR`

Purpose: Shows whether the application is configured
to use a different knowledge directory.

Day 11 observation:

B2D_KNOWLEDGE_DIR=/tmp/b2d-empty

This incorrect location caused the application
to load zero knowledge documents.

Expected configuration:

/app/knowledge

If the variable is not set, the application
uses its default knowledge directory.

Important: Replace ACTUAL_CONTAINER_NAME with
the actual running container name.

### 4. Check the Knowledge Documents

First, identify the running container:

`docker ps`

Then inspect the knowledge folder:

`docker exec ACTUAL_CONTAINER_NAME ls -la /app/knowledge`

Purpose: Lists the files inside the application's default knowledge directory.

Expected files:

* `attendance-policy.txt`
* `career-guide.txt`
* `student-handbook.txt`

What to investigate: If the documents exist but `/ready` still returns 503, check whether `B2D_KNOWLEDGE_DIR` points to a different folder.

Important: Replace `ACTUAL_CONTAINER_NAME` with the name of the running container.

## Configuration Troubleshooting

If /health returns 200 but /ready returns 503,
investigate the knowledge directory configuration.

### Check 1: Environment Variable

Verify where B2D_KNOWLEDGE_DIR points.

The expected directory for our current application is:

/app/knowledge

### Check 2: Document Location

Confirm the three knowledge documents exist
inside /app/knowledge.

### Check 3: Docker Volume Mounts

Check whether a mounted directory is hiding
the documents packaged inside the Docker image.

Command:

`docker inspect ACTUAL_CONTAINER_NAME --format '{{json .Mounts}}'`

#### Compare the Running Container With the Original Image

Check the documents visible inside the running container:

`docker exec ACTUAL_CONTAINER_NAME ls -la /app/knowledge`

Find the exact image the affected container was created from:

`docker inspect ACTUAL_CONTAINER_NAME --format '{{.Image}}'`

This returns the image ID (sha256:...). Use the ID rather than a tag,
because a tag can be moved to a newer build after the container started.

Check that exact image independently:

`docker run --rm IMAGE_ID ls -la /app/knowledge`

This command creates a temporary container without adding
a volume mount. It lists the packaged files without starting
the FastAPI server.

Day 11 example: the test image was tagged
b2d-knowledge-assistant:day11, so the equivalent command is:

`docker run --rm b2d-knowledge-assistant:day11 ls -la /app/knowledge`

Interpreting the results:

| Running container | Original image | What to investigate |
|---|---|---|
| Empty | Three documents present | Volume mounts, files removed at runtime, or incorrect image version |
| Empty | Empty | Docker build context, COPY, or .dockerignore |
| Documents present | Documents present | Knowledge directory configuration, file extensions, or document-loading errors |

Use the same image version as the running container when comparing results.

The image comparison shows only the packaged files, not changes
made inside the running container afterward. To check for files
added, changed, or removed at runtime:

`docker diff ACTUAL_CONTAINER_NAME`

Lines starting with A, C, or D show added, changed, or deleted files.
For example, `D /app/knowledge/student-handbook.txt` means the file
was deleted inside the container. Files hidden by a volume mount do
not appear here, so use the mount check above for that case.

### Determine the Cause

If the files exist but the application is looking
in another directory, investigate the environment
variable.

If the files are missing from the image itself,
investigate the Docker build and COPY instructions.

## Recommended Resolution

### Resolution 1: Incorrect Environment Variable

If B2D_KNOWLEDGE_DIR points to the wrong folder:

1. Verify that the knowledge documents exist in /app/knowledge.
2. Identify where the incorrect environment variable was configured.
3. Correct the configuration to use /app/knowledge.
4. Recreate the container with the corrected configuration.
5. Verify that /ready returns HTTP 200 with three documents.

Important: Restarting the existing container does not change
its environment variables. A new container must be created
with the corrected settings.

### Resolution 2: Incorrect Docker Volume Mount

If a mounted directory is hiding the knowledge documents:

1. Inspect the container's mounts to identify what is
   mounted over /app/knowledge.
2. Compare the running container's files with the files
   packaged in the original Docker image.
3. Confirm whether the mount was intentional.
4. If the mount is incorrect, update the Docker
   deployment configuration.
5. Recreate the container with the corrected mount.
6. Test /ready and /documents to verify the fix.

Important: Never delete a district's mounted folder
or its contents without verifying ownership, purpose,
and backups. It may contain important school data.

### Resolution 3: Missing Documents in the Docker Image

If the original Docker image does not contain the knowledge documents:

1. Check whether the knowledge files exist on the build machine.
2. Verify that the Dockerfile includes:
   `COPY knowledge/ ./knowledge/`
3. Check whether .dockerignore excludes the knowledge folder or .txt files.
4. Confirm that the correct build context was used.
5. Rebuild the image with the corrected files and configuration.
6. Create a new container from the corrected image.
7. Verify /ready returns HTTP 200 and the expected documents are loaded.

Important: Rebuilding the Docker image is appropriate when
the image itself is missing required application files.

## Verifying the Fix

After applying a fix, verify that the B2D Knowledge Assistant
is functioning correctly.

### 1. Verify Application Health

Command: `curl -i http://127.0.0.1:8002/health`

Expected: HTTP 200 with `{"status":"ok"}`.

### 2. Verify Application Readiness

Command: `curl -i http://127.0.0.1:8002/ready`

Expected: HTTP 200 with
`{"status":"ready","document_count":3}`.

### 3. Verify Knowledge Documents

Command: `curl -i http://127.0.0.1:8002/documents`

Expected documents:
- attendance-policy.txt
- career-guide.txt
- student-handbook.txt

### 4. Verify Document Retrieval

Send a question to the Knowledge Assistant:

```bash
curl -i -X POST http://127.0.0.1:8002/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the attendance policy?"}'
```

Expected results:

- HTTP 200 OK
- Source: attendance-policy.txt
- Retrieval score greater than 0
- Context contains the relevant attendance policy

If the wrong document is returned, investigate the retrieval
logic before marking the incident resolved.

### 5. Record Evidence

Save only the information necessary to demonstrate that the
application works correctly.

Information to record:

- HTTP status codes (200, 503, etc.).
- Readiness status and document count.
- Retrieved document source filename, when approved for logging.
- Retrieval matching score.
- Test timestamp and relevant non-sensitive errors.

Do not record:

- Full student questions or assistant responses.
- Retrieved document contents or the `context` field.
- Student names, attendance records, or personal information.
- API keys, authentication tokens, or sensitive HTTP headers.

Use approved synthetic test questions when verifying retrieval.

Only share sanitized evidence with authorized district personnel.
Follow the district's data retention and access policies.

Do not mark the incident resolved until the required checks pass
and the affected functionality is verified.

Note: Port 8002 was used in the Day 11 local experiment.
For a district deployment, use the actual configured address
and published port.

## Privacy and Logging Rules

The B2D Knowledge Assistant may be used in school
environments, so application logs must be handled carefully.

### What We Can Log

- HTTP status codes such as 200 and 503.
- Application readiness status.
- Number of available knowledge documents.
- Request timestamps and response times.
- Error types needed for troubleshooting.

### What We Should Not Log

- Student names or identifying information.
- Student grades, attendance records, or personal details.
- Full user questions containing private information.
- API keys, passwords, or access tokens.
- Confidential school documents or their contents.

### Logging Security

- Limit log access to authorized personnel.
- Follow district retention and deletion policies.
- Never share sensitive logs in public GitHub repositories.
- Remove sensitive information before sharing incident reports.

### FDE Responsibility

Collect enough evidence to troubleshoot application failures
without unnecessarily exposing student or district information.

## When to Escalate

### Escalation Conditions

Escalate the incident when:

1. The /ready endpoint continues returning 503
   after checking the knowledge directory and
   deployment configuration.

2. The application returns HTTP 500 errors
   or repeatedly crashes.

3. The assistant retrieves incorrect school policies
   after troubleshooting.

4. There is evidence of unauthorized access,
   exposed credentials, or possible student data leakage.

5. The incident affects multiple schools or
   prevents staff from accessing critical information.

### Who to Contact

- Application errors: B2D development team.
- Docker or hosting problems: Infrastructure engineer.
- Potential data exposure: District security/privacy
  contact and the designated B2D security contact.
- Extended service disruptions: District technology
  director and B2D project lead.

### Information to Include

- When the problem was detected.
- Which endpoints failed.
- Relevant HTTP status codes.
- Container and image identification.
- Troubleshooting steps already performed.
- Business impact on the school.
- Sanitized logs or error messages.

### Important Rule

Do not mark an incident resolved until the required
application checks pass and the customer confirms
that the affected functionality is restored.
