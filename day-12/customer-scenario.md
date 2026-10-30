# Day 12 Customer Incident Scenario

## Customer Problem

The district's B2D Knowledge Assistant container is running, but Docker reports it as unhealthy, and teachers can't find school policies. The IT administrator wants to know whether to restart the container and whether Docker itself is broken.

## What the Evidence Tells Me

Docker is working correctly. The container's HEALTHCHECK calls `/ready`, which returns HTTP 503 whenever `load_documents()` finds zero documents, so Docker marks the container unhealthy. `/health` returning 200 only proves the app process is alive. Together, the evidence says the app is running but has no knowledge documents to search, which is why teachers get no policy answers.

## Investigation Steps

Before changing anything, I would gather read-only evidence:

1. `docker inspect` the container to check the `B2D_KNOWLEDGE_DIR` environment variable and any volume or bind mounts on the knowledge path. A mount over `/app/knowledge` hides the documents baked into the image, and an empty mount produces exactly this symptom.
2. `docker exec` into the container and list the knowledge directory to confirm what files actually exist, along with their owners and permissions. The app runs as non-root `appuser` (UID 10001), so it must be able to read them.
3. Check the file extensions. The loader only reads `*.txt`, so policies uploaded as PDF or Word files would count as zero documents.
4. Review `docker logs` for startup or file-read errors (for example, permission denied or an encoding error) and ask the district what changed recently, such as a redeploy, a new mount, or a document upload.

## Recommended Resolution

The fix depends on the root cause I confirm. If the environment variable or mount points to the wrong or an empty location, I would correct the configuration and recreate the container. If the files are present but unreadable, I would fix ownership or permissions for UID 10001. If they're in an unsupported format, I would convert them to `.txt`. A plain restart alone isn't recommended, because the container would come back with the same configuration and still find zero documents.

## Verification Before Closing

I would confirm that `/ready` returns HTTP 200 with the expected document count, that `/documents` lists the district's policy files, and that `docker ps` shows the container as healthy after the health check interval. Then I would run a realistic teacher query, such as "What is the attendance policy?", through `/ask` and confirm it returns the correct source. Finally, I would ask the IT administrator to confirm that a teacher can find a policy before I close the ticket.

## Customer-Facing Explanation

"The assistant itself is running, and Docker is working as designed. Its built-in check noticed that the assistant can't currently see its library of school documents, which is why teachers aren't getting answers. Restarting wouldn't fix that by itself, so we're confirming where the documents should be loaded from, correcting that setting, and testing with a real policy question before we call it resolved."

## Privacy and Security Considerations

My troubleshooting notes should record status codes, document counts, file names, and configuration paths, not the contents of district documents or the full text of teacher questions, which could contain student or staff information. I would never paste API keys, passwords, tokens, or full environment dumps into logs or tickets. Any fix should keep the container running as the non-root user rather than switching to root to work around a permissions problem.
