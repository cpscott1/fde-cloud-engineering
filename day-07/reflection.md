# Day 7 Reflection — Retrieval Evaluations, Logging, and Python Practice

## Day 7 Objective

The main goal for Day 7 was to learn how to evaluate whether the B2D Cloud AI Knowledge Assistant retrieves the correct document, instead of only assuming that retrieval works because a few manual questions returned good answers.

I also learned how logging can help me understand what the application is doing while it runs.

The biggest shift today was moving from:

> “The retrieval system seems to work.”

to:

> “I can test it, measure it, identify failures, and record what happened.”

That feels like an important step toward thinking more like a Forward Deployed AI Engineer.

---

# What I Started With

At the beginning of Day 7, I already had a simple retrieval system from Day 6.

The basic flow was:

```text
User question
      |
      v
search_documents()
      |
      v
Load knowledge files
      |
      v
Tokenize the question and documents
      |
      v
Compare matching words
      |
      v
Calculate a score
      |
      v
Return the best document
```

The system could return a result like:

```python
{
    "source": "student-handbook.txt",
    "context": "Student handbook content...",
    "score": 5
}
```

It could also return:

```python
{
    "source": None,
    "context": None,
    "score": 0
}
```

when no useful match existed.

Day 7 focused on testing whether that behavior was correct.

---

# New Concept: Evaluation

The biggest new concept today was an **evaluation**, often shortened to **eval**.

An evaluation is a test that compares:

```text
What I expected the system to return
```

against:

```text
What the system actually returned
```

I created test cases like:

```python
{
    "question": "What is the attendance policy?",
    "expected_source": "attendance-policy.txt"
}
```

This dictionary acts like an answer key.

The question is:

```text
What is the attendance policy?
```

and the document I expect the system to retrieve is:

```text
attendance-policy.txt
```

---

# Expected vs. Actual Results

I learned to separate the expected result from the actual result.

Example:

```python
expected_source = test_case["expected_source"]
actual_source = result["source"]
```

The expected result is what I believe should happen.

The actual result is what the retrieval system really returned.

Then I compared them with:

```python
is_correct = actual_source == expected_source
```

This produces a Boolean:

```text
True
```

or:

```text
False
```

If they match, the test passes.

If they do not match, the test fails.

---

# PASS and FAIL

I turned the Boolean result into something easier to read:

```python
if is_correct:
    print("PASS")
else:
    print("FAIL")
```

This gave me output like:

```text
True
PASS
```

or:

```text
False
FAIL
```

This made it much easier to see whether the retrieval system behaved correctly.

---

# My First Evaluation Cases

I tested four questions.

## Test 1

Question:

```text
What is the attendance policy?
```

Expected:

```text
attendance-policy.txt
```

Actual:

```text
attendance-policy.txt
```

Result:

```text
PASS
```

---

## Test 2

Question:

```text
Can students use phones during class?
```

Expected:

```text
student-handbook.txt
```

Actual:

```text
student-handbook.txt
```

Result:

```text
PASS
```

---

## Test 3

Question:

```text
What is for lunch tomorrow?
```

Expected:

```text
None
```

Actual:

```text
None
```

Result:

```text
PASS
```

This test was important because I learned that a no-match result can still be the correct result.

The system did not have lunch information in the knowledge base, so returning no document was the correct behavior.

That is safer than inventing an answer.

---

## Test 4

Question:

```text
Are cellphones allowed?
```

Expected:

```text
student-handbook.txt
```

Actual:

```text
None
```

Result:

```text
FAIL
```

This failure was very useful.

The student handbook uses wording like:

```text
phones
```

while the question used:

```text
cellphones
```

A human understands that those words are related.

My current retrieval system does not understand meaning or synonyms.

It mainly depends on exact word overlap.

This showed me a real weakness in the retrieval approach.

---

# Why the Failure Was Useful

Before adding the cellphone question, my system had:

```text
3 passed
3 total
100% accuracy
```

After adding the harder question, the result became:

```text
3 passed
4 total
75% accuracy
```

The system did not suddenly get worse.

The harder test exposed a weakness that was already there.

This was an important lesson:

> A failed evaluation is not automatically bad. It can reveal where the system needs improvement.

As an FDE, I need to find weaknesses before customers depend on the system.

---

# Accuracy

I learned how to calculate accuracy using:

```python
accuracy = (passed / total) * 100
```

For my Day 7 evaluation:

```text
passed = 3
total = 4
```

So:

```text
3 / 4 = 0.75
```

and:

```text
0.75 * 100 = 75
```

The final result was:

```text
Accuracy: 75.0
```

This does not mean the AI system is “75% intelligent.”

It means:

> On these four specific retrieval tests, the expected document was returned three out of four times.

That distinction matters.

---

# Counting Passing Tests

I used a counter:

```python
passed = 0
```

Then every time a test passed:

```python
passed += 1
```

This means the same thing as:

```python
passed = passed + 1
```

The counter changed like this:

```text
0
1
2
3
```

At the end, Python printed:

```text
Passed: 3
```

This helped me understand how evaluations can automatically track results.

---

# Python Concept: Lists of Test Cases

I changed from testing one dictionary to testing a list of dictionaries.

Example:

```python
test_cases = [
    {
        "question": "What is the attendance policy?",
        "expected_source": "attendance-policy.txt"
    },
    {
        "question": "Can students use phones during class?",
        "expected_source": "student-handbook.txt"
    }
]
```

Then I used:

```python
for test_case in test_cases:
```

to evaluate each test one at a time.

This reinforced the Python concepts I practiced on Day 6.

The entire list is:

```text
test_cases
```

and during each loop:

```text
test_case
```

represents one dictionary.

---

# Python Concept: Indentation

One important thing I learned today was how much indentation matters in Python.

At one point, both questions were being evaluated, but only one `PASS` was printed.

The reason was that the `if is_correct:` block was outside the loop.

When I moved:

```python
if is_correct:
    print("PASS")
else:
    print("FAIL")
```

inside:

```python
for test_case in test_cases:
```

each test received its own PASS or FAIL result.

This helped me understand that indentation determines which code belongs inside a loop or condition.

---

# New Concept: Logging

Another major concept I learned was Python logging.

I imported:

```python
import logging
```

and created a named logger:

```python
logger = logging.getLogger("b2d.retrieval")
```

I learned that:

```text
b2d.retrieval
```

is simply a name I chose for the logger.

It helps identify which part of the application produced the message.

For example:

```text
b2d
└── retrieval
```

represents the retrieval part of the B2D application.

---

# Logging Successful Retrievals

I added:

```python
logger.info(
    "retrieval_result source=%s score=%s",
    best_document["source"],
    best_score
)
```

This produced logs like:

```text
INFO:b2d.retrieval:retrieval_result source=attendance-policy.txt score=2
```

and:

```text
INFO:b2d.retrieval:retrieval_result source=student-handbook.txt score=5
```

The log records:

```text
which document was selected
```

and:

```text
what score it received
```

---

# Logging No-Match Results

I also added:

```python
logger.info("retrieval_result source=None score=0")
```

This produced:

```text
INFO:b2d.retrieval:retrieval_result source=None score=0
```

That tells me the retrieval system ran but did not find a useful document.

This happened for:

```text
What is for lunch tomorrow?
```

and:

```text
Are cellphones allowed?
```

The important difference is that the lunch question was an expected no-match, while the cellphone question was an unexpected no-match.

That is why evaluations are important.

Logging alone tells me what happened.

Evaluations tell me whether what happened was correct.

---

# Logging Configuration

Inside `eval_retrieval.py`, I added:

```python
logging.basicConfig(level=logging.INFO)
```

I learned that this line configures logging so INFO messages are visible.

The relationship is:

```text
retrieval.py
→ creates INFO log messages

eval_retrieval.py
→ configures Python to display INFO messages
```

This helped me understand that:

```python
logger.info(...)
```

creates the message,

while:

```python
logging.basicConfig(level=logging.INFO)
```

helps control what logging levels are shown.

---

# Understanding the Log Format

I saw output like:

```text
INFO:b2d.retrieval:retrieval_result source=student-handbook.txt score=5
```

I learned to break that into three parts.

## INFO

```text
INFO
```

is the logging level.

It means this is normal informational activity.

## b2d.retrieval

```text
b2d.retrieval
```

is the logger name.

It identifies which part of the application produced the message.

## retrieval_result...

```text
retrieval_result source=student-handbook.txt score=5
```

is the actual message.

---

# Logging and Cloud Engineering

Logging connects directly to Learn to Cloud.

Locally, I can see the logs in my terminal.

Later, the same concept can work like:

```text
Python application
      |
      v
Docker container
      |
      v
Cloud service
      |
      v
Application logs
      |
      v
Monitoring and troubleshooting
```

This means that if the B2D assistant is deployed somewhere and starts behaving incorrectly, I should not have to guess what happened.

Logs can help me investigate.

---

# Logging and Privacy

I also learned that logging can create security and governance concerns.

I intentionally logged:

```text
source
score
```

instead of automatically logging:

```text
full student question
student name
private records
full document content
```

This matters because a real education system may process sensitive information.

An FDE needs to think about both:

```text
What information would help troubleshoot?
```

and:

```text
What information should not be stored unnecessarily?
```

---

# Python Refresher

The Day 7 Python refresher focused on concepts I was already using inside the evaluation system.

---

## Booleans

I practiced:

```python
expected_source = None
actual_source = None

is_correct = actual_source == expected_source

print(is_correct)
```

The result was:

```text
True
```

This reinforced that a Boolean is either:

```text
True
```

or:

```text
False
```

---

## Comparison with `==`

I reinforced the difference between:

```python
=
```

and:

```python
==
```

A single equals sign stores a value:

```python
score = 2
```

A double equals sign compares values:

```python
score == 2
```

Python uses:

```python
==
```

for equality comparison.

Unlike JavaScript, Python does not require:

```text
===
```

---

## Counting Boolean Results

I practiced:

```python
results = [
    True,
    True,
    False,
    True
]
```

Then:

```python
passed = 0

for result in results:
    if result == True:
        passed += 1
```

The result was:

```text
3
```

I also learned that because `result` is already a Boolean, this can be simplified to:

```python
if result:
```

---

## Accuracy Practice

I practiced:

```python
passed = 3
total = 4
```

Then:

```python
accuracy = (passed / total) * 100
```

The output was:

```text
75.0
```

This directly matches the logic used by my evaluation script.

---

# Customer Scenario

The Day 7 customer scenario involved a teacher asking:

> Are cellphones allowed?

The knowledge base contains a phone policy in:

```text
student-handbook.txt
```

but the retrieval system returned:

```text
None
```

The issue was not that the document was missing.

The issue was that the user phrased the question differently than the wording used in the document.

This is a realistic customer problem.

A teacher should not need to know exactly how the handbook phrases something before they can retrieve the correct information.

---

# FDE Troubleshooting View

For the cellphone failure, I can think through the system layer by layer.

```text
Was Python running?
Yes.

Did the evaluation script run?
Yes.

Did search_documents() execute?
Yes.

Were the knowledge documents available?
Yes.

Did logging show retrieval activity?
Yes.

Did the correct policy exist?
Yes.

Did retrieval select it?
No.
```

This narrows the problem down to:

```text
retrieval quality
```

rather than:

```text
networking
FastAPI
server process
missing file
Python crash
```

That is a more disciplined troubleshooting process.

---

# Governance Lesson

The safe behavior for the failed cellphone query was still:

```text
None
```

rather than inventing a policy.

That is important.

The system currently fails to retrieve some correct answers, but it does not automatically manufacture information when retrieval produces no useful match.

For an education assistant, that behavior is preferable to confidently giving a policy that does not exist.

---

# What I Understand Better After Day 7

I now understand that:

- An evaluation tests whether the system behaved as expected.
- `expected_source` is the answer I believe should be correct.
- `actual_source` is what retrieval really returned.
- `==` compares two values.
- A comparison produces `True` or `False`.
- PASS and FAIL make evaluation results easier to read.
- A list can contain multiple evaluation dictionaries.
- A loop allows the same test logic to run repeatedly.
- Indentation controls what runs inside a loop.
- A counter can track how many tests pass.
- Accuracy can be calculated from passed tests divided by total tests.
- 75% accuracy only applies to the specific tests I created.
- A failed test can reveal an important weakness.
- Logging helps show what happened while an application ran.
- Logging and evaluations solve different problems.
- Logs should avoid unnecessary sensitive information.
- Exact keyword retrieval can struggle with synonyms.
- No-match behavior can be the correct and safest result.

---

# Day 7 FDE Takeaway

The biggest lesson from Day 7 is:

> I should not judge an AI system only by a few successful demos. I need repeatable tests that prove whether the system behaves correctly.

Another important lesson is:

> Observability matters because when something fails, I need evidence showing what the application actually did.

As an FDE, I should be able to explain:

```text
What did the customer ask?

What did we expect?

What did the system actually do?

Did it pass or fail?

What logs do we have?

What layer caused the failure?

What is the customer impact?

What should we improve?
```

That is much stronger than simply saying:

> The AI gave the wrong answer.

---

# Current B2D Cloud AI Knowledge Assistant Progress

The application now has two related workflows.

## Customer/application workflow

```text
Question
   |
   v
FastAPI
   |
   v
search_documents()
   |
   v
Knowledge files
   |
   v
Keyword comparison
   |
   v
Best source + context + score
```

## Evaluation workflow

```text
Known test question
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
Compare expected vs actual
   |
   v
PASS / FAIL
   |
   v
Passed / Total / Accuracy
```

And logging now gives visibility into retrieval behavior:

```text
search_documents()
      |
      v
logger.info(...)
      |
      v
source + score
```

---

# Current Evaluation Baseline

Current results:

```text
Passed: 3
Total: 4
Accuracy: 75.0%
```

Known failing query:

```text
Are cellphones allowed?
```

Expected:

```text
student-handbook.txt
```

Actual:

```text
None
```

Known limitation:

> The current retrieval system relies heavily on exact normalized word overlap and does not yet understand synonyms or semantic similarity.

---

# What I Should Not Do Yet

I do not need to immediately add an LLM just because one evaluation failed.

The failure tells me that the retrieval layer needs improvement.

A better engineering process is:

```text
Establish baseline
      |
      v
Identify failure
      |
      v
Make one change
      |
      v
Run evaluations again
      |
      v
Compare results
```

This lets me prove whether a change actually helped.

---

# Next Step

The next step should build from the 75% retrieval baseline.

I should preserve the failing cellphone test and use it as a regression test.

The next retrieval improvement could explore a small controlled improvement such as:

```text
cellphone
→ phone

cellphones
→ phones
```

or another lightweight normalization technique.

Then I can rerun:

```bash
python3 eval_retrieval.py
```

and see whether:

```text
3 / 4
```

improves to:

```text
4 / 4
```

without breaking the tests that already pass.

After retrieval becomes more reliable, the project can continue toward:

```text
stronger retrieval
→ RAG
→ model integration
→ Docker
→ cloud deployment
→ CI/CD
→ security
→ governance
→ observability
```

The important thing is that future changes will now be measured instead of guessed.