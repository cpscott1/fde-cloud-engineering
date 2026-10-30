# B2D Cloud AI Knowledge Assistant Runbook

## 1. Go to the project

```bash
cd ~/fde-study-projects/fde-cloud-engineering
```

## Troubleshooting stale API behavior

If the code looks correct but the API still returns old results, check which process is using port 8000:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

There should normally be one current Python/Uvicorn process listening on port 8000.

If older processes are still listening, stop the stale processes and restart the current application.

Start the application with:

```bash
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
```

Then open a second terminal and retest the API:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Are cellphones allowed?"}'
```

Expected result:

- Source: `student-handbook.txt`
- Score: `1`
