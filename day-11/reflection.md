# Day 11 Reflection

## What I Built

I added a `/ready` endpoint to the B2D Knowledge Assistant that counts the knowledge documents and returns a 503 with `not_ready` if there are zero. Then I tested it both ways in Docker on port 8002: once with the documents in place (200, ready, 3 documents) and once with `B2D_KNOWLEDGE_DIR` pointed at `/tmp/b2d-empty` (503, 0 documents). I also wrote a full readiness runbook for district IT and a Day 11 evidence report with the real results.

## What I Learned About Liveness and Readiness

The server being up and the assistant being ready are two different things. When I broke the knowledge folder setting, `/health` still came back 200 because it never looks at the documents, but `/ready` came back 503 because there was nothing to answer from. Easiest way I'd explain it: `/health` asks "is it on?" and `/ready` asks "can it actually do its job?"

## What I Learned About Docker Configuration

Environment variables get locked in when the container is created, so if the setting is wrong you have to recreate the container, not just restart it. I also learned `docker exec ... ls` only shows what the running container sees, and a volume mount can hide files that are really in the image. To check the image itself, I'd grab the exact image ID with `docker inspect` and run `docker run --rm` against it, because a tag like `day11` can get moved to a newer build.

## What I Learned About Customer Troubleshooting

Before I fix anything I need to know which problem I'm dealing with: a bad setting, a bad mount, or files missing from the image. Each one has a different fix, and rebuilding the image is only the right call when the image is actually missing files. Big takeaway for me is not to call it fixed until `/health`, `/ready`, `/documents`, and `/ask` all check out and the district confirms it's working on their end.

## Privacy and Logging Lessons

I caught that my runbook told people to save the full HTTP responses, but `/ask` sends back the whole question and the whole document in `context`. In a real school that could put student info or confidential policies right into an incident report. So now I only record status codes, readiness, document count, score, and the source filename when that's approved, and I test with made-up questions.

## Biggest Challenge

Keeping straight what's in the Docker image versus what the running container is actually seeing. My first instinct was that an empty folder meant the files never got packaged, but it could just as easily be a mount, a setting, or someone deleting files at runtime. Slowing down and checking the image and the container separately is what cleared it up for me.

## Next Step

Take the runbook and the evidence report and treat them like something I'd actually hand to a district. After that, keep building on `/ask` testing, because one question pulling the right document doesn't prove the assistant gives good answers across the board.
