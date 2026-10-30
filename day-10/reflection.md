# Day 10 Reflection

## What I built
- Docker image: b2d-knowledge-assistant:day10 (python:3.12-slim base, 239MB on disk, FastAPI + uvicorn on port 8000)
- Application endpoints tested: GET /health, GET /documents, POST /ask
- Knowledge documents verified: attendance-policy.txt, career-guide.txt, student-handbook.txt

## What I learned about Docker
1. What is the difference between an image and a container?

   The image is the blueprint. It's the packaged, read-only snapshot of everything the app needs: Python, my dependencies, app.py, retrieval.py, and the knowledge folder. The container is an instance of that image. It can be running or stopped, and a stopped container still exists until I remove it. I can spin up multiple containers from the same image, and if I stop or delete a container, the image is still sitting there ready to go again. Easiest way I'd explain it to a student: the image is the recipe, the container is the meal.

2. What does port mapping 8001:8000 mean?

   Left side is my machine, right side is inside the container. So 8001:8000 means "when I hit localhost:8001 on my Mac, send that traffic to port 8000 inside the container," which is where uvicorn is listening. The app itself has no idea 8001 exists. That's why I can run the same image on a different host port without touching the code.

3. What did I learn from the invalid port error?

   Docker checks the port mapping before it ever starts the container, so a bad port fails right away instead of failing quietly later. Ports have to be a real number in range (1 to 65535) and in the right host:container order. Big takeaway for me is to actually read the error message. It told me exactly what was wrong, and that's a habit I want to bring to customer issues too: read the error before you start guessing.

## What I learned about Python
1. How does Path.exists() work?

   You wrap a file path in Path() and call .exists() on it. It checks if that file or folder is really there and gives back True or False. It doesn't open or read the file, it just answers "is this here or not." I also learned I can write `if not item_path.exists():` instead of `== False`, which reads cleaner.

2. What does find_missing_files() return?

   It returns a list of every file from the list I passed in that doesn't exist. If everything is there, I get back an empty list `[]`. When I tested it with "app.py" and "another-missing-file.txt", it gave me back just the missing one. So it tells me exactly WHAT is missing, not just that something is.

3. What does ready_to_build() return?

   It returns a single True or False. True means every required file is there and I'm good to build. False means at least one file is missing. It's a yes/no gate, where find_missing_files() is the detailed report.

4. Why must return True be outside the loop?

   Because `return` ends the function on the spot. If I put `return True` inside the loop, it would check the first file, see it's there, and say "ready" without ever looking at the rest. That's a false positive, and it's the worst kind of bug because it looks like it's working. The only way I can honestly say "everything is good" is after the loop has checked every single file. Inside the loop, the only early exit should be `return False` the moment I find something missing.

## Customer Scenario
What should an FDE investigate when /health works but /documents is empty?

First thing is understanding that /health working doesn't mean the app is ready. In my code /health just returns `{"status": "ok"}`. It never touches the knowledge folder, so it only proves the server started. /documents comes back empty with no error because `glob("*.txt")` just finds nothing and returns an empty list. The app fails silently.

So I'd go down the list:
- `docker exec <container> ls -la /app/knowledge` to see if the files are actually in the container
- Check if `B2D_KNOWLEDGE_DIR` is set and pointing somewhere that doesn't exist
- Check if a volume is mounted over /app/knowledge and hiding the files that were baked into the image
- Check the file types. A .pdf, .docx, or even NOTES.TXT in caps won't match `*.txt`
- Confirm they're running the right image tag and that the knowledge folder wasn't left out by the build or .dockerignore

Then the real fix is making the app tell on itself. Add a readiness check so the problem shows up as a clear failure instead of an empty list somebody has to dig into.

## Biggest Challenge
What was the hardest part of Day 10, and how did I solve it?

The hardest part for me was the logic in ready_to_build(), specifically where `return True` goes. My instinct was to return as soon as a file checked out, and that would've made the function lie. What helped was walking through it one file at a time in my head and asking "has it actually checked everything yet?" Once I tested it with a real file list and a list with a missing file, seeing True and then False confirmed it was right. Same thing with Docker: slowing down and reading the error output told me what I needed to fix instead of me guessing.

## Next Step
Implement and test an application readiness endpoint.

Build a /ready endpoint that uses the same idea as ready_to_build(). It should check that the knowledge folder exists and actually has .txt files in it, and return a failure status if it doesn't, so /health answers "is the server up" and /ready answers "are the requirements I programmed it to check actually in place." Even if /ready passes, that doesn't guarantee every question gets a correct answer. That's what evaluations and deeper monitoring are for later. Then test it both ways: once with the documents in place, and once with them missing, to make sure it fails loud instead of silent.
