# Day 8 Reflection — Retrieval Normalization, Runtime Debugging, and Deployment Readiness

## Day 8 Objective

The main goal for Day 8 was to improve the B2D Cloud AI Knowledge Assistant retrieval system using a small normalization rule, verify that the improvement actually helped, and then make the application easier to run consistently outside of my current terminal session.

Day 8 also introduced an important deployment lesson:

> Correct code on disk does not always mean the running application is using the newest code.

By the end of the day, I had:

- improved retrieval from `3/4` passing tests to `4/4`,
- added word normalization,
- verified the fix through both the evaluation script and the live FastAPI API,
- recorded Python dependencies,
- verified the Python environment,
- documented how to run and troubleshoot the application,
- and diagnosed a stale-process problem using `lsof`.

---

# Starting Point

At the end of Day 7, the retrieval evaluation baseline was:

```text
Passed: 3
Total: 4
Accuracy: 75.0%
```

The failing question was:

```text
Are cellphones allowed?
```

Expected source:

```text
student-handbook.txt
```

Actual result:

```text
None
```

The handbook used the word:

```text
phones
```

while the question used:

```text
cellphones
```

My keyword retrieval system did not understand that those words referred to the same concept.

---

# New Concept: Word Normalization

Day 8 introduced normalization.

Normalization means converting different forms of a word into one consistent form before comparing them.

I added:

```python
WORD_NORMALIZATION = {
    "cellphone": "phone",
    "cellphones": "phone",
    "phones": "phone"
}
```

This means:

```text
cellphone  → phone
cellphones → phone
phones     → phone
```

The goal was to make the question and document use the same normalized word.

---

# Updating `tokenize()`

The original tokenizer mostly:

1. converted text to lowercase,
2. removed punctuation,
3. split the text into words,
4. removed stop words.

I changed it so each word also passes through the normalization dictionary.

The new flow is:

```text
Raw text
   ↓
Lowercase
   ↓
Remove punctuation
   ↓
Split into words
   ↓
Normalize each word
   ↓
Remove stop words
   ↓
Return useful words
```

For example:

```text
Are cellphones allowed?
```

becomes:

```text
are cellphones allowed
```

then:

```python
["are", "cellphones", "allowed"]
```

then normalization changes:

```text
cellphones → phone
```

which produces:

```python
["are", "phone", "allowed"]
```

After removing the stop word `are`, the useful words become approximately:

```python
{"phone", "allowed"}
```

---

# Understanding `.get(word, word)`

One of the most important Python concepts today was:

```python
WORD_NORMALIZATION.get(word, word)
```

The first `word` means:

> Look for this word as a key in the dictionary.

The second `word` means:

> If the key is not found, return the original word.

So:

```python
WORD_NORMALIZATION.get("cellphones", "cellphones")
```

returns:

```text
phone
```

because `cellphones` exists in the dictionary.

But:

```python
WORD_NORMALIZATION.get("attendance", "attendance")
```

returns:

```text
attendance
```

because `attendance` does not exist in the dictionary.

This is useful because only known word variants are changed.

Everything else stays unchanged.

---

# Verifying the Tokenizer

I tested:

```python
tokenize("Are cellphones allowed?")
```

and got:

```python
{'phone', 'allowed'}
```

This confirmed that:

```text
cellphones
```

was successfully normalized to:

```text
phone
```

before retrieval scoring happened.

---

# Retrieval Evaluation Improvement

After adding normalization, I reran:

```bash
python3 eval_retrieval.py
```

The results changed from:

```text
Passed: 3
Total: 4
Accuracy: 75.0
```

to:

```text
Passed: 4
Total: 4
Accuracy: 100.0
```

The previously failing query:

```text
Are cellphones allowed?
```

now returned:

```text
student-handbook.txt
```

with:

```text
score = 1
```

The log showed:

```text
INFO:b2d.retrieval:retrieval_result source=student-handbook.txt score=1
```

This proved that normalization improved the current evaluation suite.

---

# Important Evaluation Lesson

The result:

```text
4 / 4
100%
```

does not mean the retrieval system is perfect.

It means:

> The system passed all four test cases currently in the evaluation suite.

The knowledge base is still small.

The evaluation suite is still small.

Many possible questions, synonyms, misspellings, and ambiguous queries have not been tested yet.

So the 100% result is a baseline, not proof that the system will work for every real-world question.

---

# Python Environment Verification

I activated the project virtual environment:

```bash
source .venv/bin/activate
```

The terminal showed:

```text
(.venv)
```

I verified which Python interpreter was active:

```bash
which python3
```

and confirmed it pointed inside:

```text
fde-cloud-engineering/.venv/bin/python3
```

I also verified the Python version:

```text
Python 3.14.7
```

This confirmed that the project was using the intended virtual environment instead of another Python installation on the Mac.

---

# Recording Dependencies

I created:

```text
requirements.txt
```

using:

```bash
python3 -m pip freeze > requirements.txt
```

This command:

```text
uses the current Python environment
→ asks pip which packages are installed
→ records their versions
→ writes them into requirements.txt
```

The file included packages such as:

```text
fastapi
pydantic
httpx
```

along with their installed versions and dependencies.

I then ran:

```bash
python3 -m pip check
```

and received:

```text
No broken requirements found.
```

This confirmed that the current environment did not report broken dependency relationships.

---

# Why `requirements.txt` Matters

My local machine already has the needed packages installed.

A different machine does not automatically have them.

A deployment environment needs a way to know which dependencies the application requires.

That is one purpose of:

```text
requirements.txt
```

This supports the move toward reproducible environments.

---

# FastAPI Runtime Verification

I started the application with:

```bash
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
```

I learned that:

```text
python3 -m uvicorn
```

runs Uvicorn using the active Python environment.

```text
app:app
```

means:

```text
app.py
→ FastAPI object named app
```

```text
--host 0.0.0.0
```

means the server listens on all available network interfaces.

```text
--port 8000
```

means the application listens on port 8000.

---

# Verifying the API

I tested the health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

and received:

```json
{"status":"ok"}
```

I tested the documents endpoint:

```bash
curl http://127.0.0.1:8000/documents
```

and received:

```json
{
  "documents": [
    "attendance-policy.txt",
    "student-handbook.txt",
    "career-guide.txt"
  ]
}
```

This verified that the running application could see all three knowledge files.

---

# Unexpected Runtime Problem

When I tested:

```text
Are cellphones allowed?
```

through the live FastAPI `/ask` endpoint, I initially received:

```json
{
  "question": "Are cellphones allowed?",
  "source": null,
  "context": null,
  "score": 0
}
```

This was confusing because the evaluation script already showed:

```text
PASS
```

for the same question.

I then tested the retrieval function directly with:

```bash
python3 -c 'from retrieval import search_documents; print(search_documents("Are cellphones allowed?"))'
```

and it correctly returned:

```text
student-handbook.txt
score 1
```

This proved that the current retrieval code was working.

The problem was somewhere in the running application process.

---

# Process Troubleshooting

I checked which processes were listening on port 8000:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

The output showed multiple Python processes listening on the same port.

This meant older Uvicorn processes were still running.

Those older processes had loaded an earlier version of the retrieval code.

So even though:

```text
retrieval.py
```

was correct on disk, the live API was still serving stale behavior.

---

# Fixing the Runtime Issue

I stopped the stale processes and restarted one clean Uvicorn process.

After restarting, I verified:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

and saw one active Python process listening on:

```text
*:8000
```

I then reran the API request:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Are cellphones allowed?"}'
```

The live API now returned:

```json
{
  "question": "Are cellphones allowed?",
  "source": "student-handbook.txt",
  "context": "Student handbook: Phones must remain stored during class unless a teacher authorizes their use. Students may use school devices for approved instructional activities.",
  "score": 1
}
```

This confirmed that the live API was finally using the current Day 8 code.

---

# Major FDE Troubleshooting Lesson

This was one of the most important lessons from Day 8.

A system can have:

```text
correct source code
```

while the running service still behaves incorrectly.

The problem might be:

```text
runtime
process
port
environment
configuration
stale application version
```

rather than the code itself.

A useful troubleshooting flow is:

```text
Does the direct function work?
        ↓
Does the evaluation test work?
        ↓
Does the API behave the same way?
        ↓
If not, inspect the running process.
```

This prevents me from changing working code because of a deployment or runtime issue.

---

# Local Troubleshooting vs. Production

Using:

```bash
lsof
```

and manually stopping stale processes is useful for understanding local runtime behavior.

It is not the long-term production model.

In production, I eventually want:

```text
container
→ controlled process
→ health check
→ automated restart
→ centralized logs
→ managed deployment
```

This is one reason Docker is the next logical infrastructure step.

Containerization helps reduce:

```text
"It works in my terminal."
```

and moves toward:

```text
"The same packaged runtime works consistently elsewhere."
```

---

# Runbook

I created:

```text
runbook.md
```

to document how to:

- enter the project,
- start the API,
- inspect port 8000,
- identify stale processes,
- restart the application,
- and retest the `/ask` endpoint.

This matters because deployment knowledge should not exist only in my memory.

Another engineer or future version of me should be able to follow the instructions.

---

# Deployment Readiness Documentation

I also created:

```text
deployment-readiness.md
```

to capture:

- the verified Python environment,
- dependency status,
- evaluation baseline,
- API behavior,
- retrieval improvement,
- runtime troubleshooting incident,
- and the next step toward Docker.

This turns the work from an informal coding exercise into documented engineering evidence.

---

# Python Refresher

The Day 8 Python refresher focused on the same normalization logic used in the real application.

---

## Reusable Normalization Function

I created:

```python
def normalized_word(word):
    return words.get(word, word)
```

This means:

```text
take one word
→ look it up in the normalization dictionary
→ return the replacement if one exists
→ otherwise return the original word
```

For example:

```python
normalized_word("cellphones")
```

returns:

```text
phone
```

while:

```python
normalized_word("attendance")
```

returns:

```text
attendance
```

---

# Understanding `return`

Inside:

```python
def normalized_word(word):
    return words.get(word, word)
```

`return` sends the result back to the code that called the function.

It also ends the function.

This allows the result to be reused in other code.

For example:

```python
print(normalized_word("cellphones"))
```

can print:

```text
phone
```

and:

```python
normalized_words.append(normalized_word(word))
```

can store the returned result.

---

# Looping Through Words

I created:

```python
question_words = [
    "are",
    "cellphones",
    "allowed",
    "during",
    "class"
]
```

Then:

```python
for word in question_words:
    print(normalized_word(word))
```

produced:

```text
are
phone
allowed
during
class
```

Only:

```text
cellphones
```

changed.

The other words stayed the same.

---

# Building a New List

Instead of only printing each normalized word, I created:

```python
normalized_words = []
```

Then used:

```python
for word in question_words:
    normalized_words.append(normalized_word(word))
```

The result was:

```python
['are', 'phone', 'allowed', 'during', 'class']
```

This helped me understand the difference between:

```text
printing data
```

and:

```text
storing processed data for later use
```

---

# Understanding `.append()`

`.append()` adds one item to the end of an existing list.

So:

```python
normalized_words.append(normalized_word(word))
```

means:

```text
normalize the current word
→ take the returned result
→ add it to normalized_words
```

The list grows one item at a time.

---

# Day 8 Python Checkpoint

I now understand that:

- `.get(word, word)` performs a dictionary lookup with a fallback.
- The first `word` is the key being searched.
- The second `word` is the fallback value.
- `return` sends data back from a function.
- A loop can call a function repeatedly.
- `.append()` stores each returned result in a list.
- Printing shows data, while storing data allows the program to use it later.
- Normalization helped retrieval because different word forms became comparable.
- Passing 4/4 evaluations proves only that the four current tests pass.

---

# Governance and Logging

The retrieval logs currently record information like:

```text
source
score
```

For example:

```text
INFO:b2d.retrieval:retrieval_result source=student-handbook.txt score=1
```

This is useful for troubleshooting.

The logs do not need to automatically include:

```text
student names
private student records
full sensitive questions
full document contents
```

This connects technical observability to privacy and governance.

An FDE should ask:

```text
What information helps me troubleshoot?
```

and also:

```text
What information should I avoid storing unnecessarily?
```

---

# What I Understand Better After Day 8

I now understand that:

- Retrieval quality should be measured before and after changes.
- Normalization can improve exact keyword retrieval.
- Dictionary `.get()` can provide a safe fallback.
- Functions help make logic reusable.
- `.append()` can build a new processed list.
- Passing evaluations do not prove universal correctness.
- Virtual environments isolate project dependencies.
- `requirements.txt` records installed package versions.
- `pip check` checks dependency consistency.
- Uvicorn is the process serving my FastAPI application.
- A port can have stale processes attached to it.
- Source code and running processes are separate things.
- Restarting a service may be required after code changes.
- Runtime debugging is different from code debugging.
- A runbook documents how to operate and troubleshoot a service.
- Containers can improve runtime consistency.

---

# Day 8 FDE Takeaway

The biggest lesson from Day 8 is:

> A good engineer does not stop when the code looks correct. The running system has to be verified too.

Another major lesson is:

> Improvements should be measured.

The retrieval change was useful because I could compare:

```text
Before:
3/4
75%
```

against:

```text
After:
4/4
100%
```

Then I verified that the improvement also worked through the actual API.

That gave me evidence across three layers:

```text
retrieval function
→ evaluation suite
→ live FastAPI endpoint
```

---

# Current B2D Cloud AI Knowledge Assistant Architecture

The current application flow is:

```text
User question
      |
      v
FastAPI /ask
      |
      v
search_documents()
      |
      v
tokenize()
      |
      v
word normalization
      |
      v
knowledge documents
      |
      v
word comparison
      |
      v
retrieval score
      |
      v
best document
      |
      v
source + context + score
```

The evaluation flow is:

```text
Test question
      |
      v
Expected source
      |
      v
search_documents()
      |
      v
Actual source
      |
      v
Expected == Actual
      |
      v
PASS / FAIL
      |
      v
Accuracy
```

The runtime flow is:

```text
Python environment
      |
      v
Uvicorn process
      |
      v
Port 8000
      |
      v
FastAPI
      |
      v
Retrieval
```

---

# Current Verified Baseline

Retrieval evaluation:

```text
Passed: 4
Total: 4
Accuracy: 100.0%
```

Verified live query:

```text
Are cellphones allowed?
```

Result:

```text
Source: student-handbook.txt
Score: 1
```

Python environment:

```text
Python 3.14.7
```

Dependency check:

```text
No broken requirements found.
```

---

# Next Step

The next infrastructure step is Docker.

The goal is to package:

```text
Python runtime
application code
dependencies
knowledge files
startup command
```

into one reproducible container image.

That will help move the project from:

```text
local Python process
```

toward:

```text
portable application runtime
```

After Docker, the project can continue toward:

```text
cloud deployment
→ CI/CD
→ stronger security
→ governance
→ observability
→ more advanced retrieval / RAG
→ model integration
→ agents and tool use
```

The key lesson is to keep measuring each change instead of assuming that newer or more complicated technology automatically improves the system.