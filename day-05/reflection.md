# Day 5 Reflection — FastAPI POST Requests, Pydantic Validation, and Python Classes

## Day 5 Objective

Today I moved from only retrieving information from an API to sending structured data into a FastAPI application.

I also learned more about the Python concepts behind Pydantic models, including:

- classes
- objects
- attributes
- `__init__`
- `self`
- methods
- dictionaries
- validation

The biggest lesson of the day was that a backend can be running correctly and still reject a request if the request does not match the expected schema.

---

# FastAPI Progress

Before today, my FastAPI application had:

```text
GET /health
GET /documents
```

Today I added:

```text
POST /ask
```

This changed the application from only returning information to also accepting information from a client.

My current request flow is:

```text
Client
  ↓
POST /ask
  ↓
JSON request body
  ↓
FastAPI
  ↓
Pydantic validation
  ↓
Python function
  ↓
JSON response
```

---

# GET vs POST

I learned that `GET` and `POST` serve different purposes.

## GET

I use `GET` when I want to retrieve information.

Examples:

```text
GET /health
GET /documents
```

Mental model:

```text
GET
↓
"Give me information."
```

## POST

I use `POST` when I want to send information to the server for processing.

Example:

```text
POST /ask
```

Mental model:

```text
POST
↓
"Here is information for you to process."
```

For the B2D Cloud AI Knowledge Assistant, `POST /ask` will eventually be how students and teachers send questions into the system.

---

# Request Bodies

I learned that a POST request can include a request body.

Example:

```json
{
  "question": "What is the attendance policy?"
}
```

The request body contains the data I want the API to process.

This will eventually become the input to the RAG and AI portion of the system.

---

# Pydantic

I learned that Pydantic is used to define and validate structured data.

My request model looked like:

```python
class QuestionRequest(BaseModel):
    question: str
```

This means the request is expected to contain:

```text
field name: question
field type: string
```

Pydantic helps prevent the application from accepting completely unstructured data.

---

# Successful Request

I successfully sent:

```json
{
  "question": "What is the attendance policy?"
}
```

and received:

```text
HTTP 200 OK
```

with a JSON response containing the question and a placeholder answer.

This confirmed:

```text
FastAPI server reachable       ✅
POST /ask route exists         ✅
Request body valid             ✅
Pydantic validation passed     ✅
Python function ran            ✅
JSON response returned         ✅
```

---

# Invalid Request

I intentionally sent:

```json
{
  "prompt": "What is the attendance policy?"
}
```

instead of:

```json
{
  "question": "What is the attendance policy?"
}
```

FastAPI returned:

```text
422 Unprocessable Content
```

The validation error showed that the required `question` field was missing.

This taught me that:

> The backend can be healthy while the request itself is invalid.

The failure happened during validation, before any AI model would have been called.

---

# Empty Object Test

I also sent:

```json
{}
```

FastAPI returned:

```text
422 Unprocessable Content
```

because the required `question` field was missing.

This confirmed that Pydantic was enforcing the required schema.

---

# Empty String Test

I sent:

```json
{
  "question": ""
}
```

FastAPI returned:

```text
200 OK
```

This was an important lesson.

Pydantic accepted the request because:

```text
question exists      ✅
question is a string ✅
```

However, the question was not useful because it was empty.

This taught me the difference between:

```text
Schema/type validation
```

and:

```text
Business-rule validation
```

My current schema checks whether the field exists and has the correct type.

It does not yet check whether the string contains useful content.

---

# HTTP Status Codes I Used Today

## 200 OK

The request succeeded.

## 404 Not Found

The server was reachable, but the requested route did not exist.

I saw this before `/ask` was added.

## 422 Unprocessable Content

The route existed and FastAPI received the request, but Pydantic rejected the body because it did not match the expected schema.

This helped reinforce my troubleshooting mindset:

> How far did the request get?

---

# Python Classes

I practiced building a regular Python class:

```python
class StudentQuestion:
```

I learned that a class is a blueprint for creating reusable objects that contain related data and behavior.

Example:

```text
StudentQuestion
↓
class / blueprint
```

Then:

```text
question1
↓
object / instance
```

---

# Objects

I created:

```python
question1 = StudentQuestion(
    "What is the attendance policy",
    "Joe",
    "12th"
)
```

This created one specific object from the `StudentQuestion` class.

That object stored:

```text
question
student_name
grade
```

---

# Attributes

I learned that attributes are values stored on an object.

For example:

```python
question1.question
question1.student_name
question1.grade
```

These are attributes of `question1`.

I also learned that an attribute is not the same thing as a dictionary key.

Example:

```python
question1.question
```

is an object attribute.

But:

```python
{
    "question": "What is the attendance policy?"
}
```

uses a dictionary key.

They can represent similar information, but they are different Python concepts.

---

# `__init__`

I learned that:

```python
def __init__(self, ...):
```

runs when a new object is created.

It initializes the object by setting its starting attributes.

For example:

```python
self.question = question
self.student_name = student_name
self.grade = grade
```

---

# `self`

I learned that `self` refers to the specific object currently being created or used.

For example:

```python
self.question
```

means:

> The `question` attribute belonging to this specific object.

This helped me understand why multiple objects created from the same class can store different values.

---

# Methods

I created:

```python
def to_dict(self):
```

inside the class.

I learned that a function defined inside a class is called a method.

The method returned:

```python
{
    "question": self.question,
    "student_name": self.student_name,
    "grade": self.grade
}
```

This converted the object's attributes into a dictionary.

---

# Connecting Regular Python Classes to Pydantic

I compared:

```python
class StudentQuestion:
    def __init__(self, question):
        self.question = question
```

with:

```python
class QuestionRequest(BaseModel):
    question: str
```

Both describe structured objects.

The difference is that Pydantic provides validation automatically.

With a regular Python class, I would have to write my own validation rules.

With Pydantic, I can define:

```python
question: str
```

and FastAPI can validate the incoming request before my endpoint logic processes it.

---

# FDE Troubleshooting Lesson

One of the most important lessons today was learning to separate different failure types.

A customer might say:

> "The AI app is broken."

But the problem could actually be:

```text
Server down
Route missing
Request body wrong
Validation failure
Application logic bug
RAG failure
LLM issue
```

Today I saw examples of several different failures:

```text
404
→ route missing

422
→ request schema invalid

200 with empty string
→ schema valid, but business rule weak
```

This reinforced the FDE question:

> **How far did the request get?**

---

# What I Understand Better Now

I now understand:

- how a client sends data to a FastAPI endpoint
- the difference between `GET` and `POST`
- what a request body is
- why Pydantic is useful
- what schema validation means
- why valid JSON can still be invalid for an API
- how a backend can be healthy while a request fails
- what a Python class is
- what an object is
- what an attribute is
- what `__init__` does
- what `self` means
- what a method is
- how object data can be converted into a dictionary

---

# Day 5 Key Takeaways

1. `GET` retrieves information.
2. `POST` sends information for processing.
3. POST requests can contain JSON request bodies.
4. Pydantic defines expected data structure and types.
5. Pydantic validation happens before application logic.
6. `422` means the request reached the route but failed validation.
7. `404` means the requested route was not found.
8. `200` means the request succeeded.
9. An empty string can still satisfy a `str` type requirement.
10. Schema validation and business validation are not the same thing.
11. A class is a blueprint for creating objects.
12. An object is a specific instance of a class.
13. Attributes store data on objects.
14. `__init__` initializes a new object.
15. `self` refers to the current object.
16. A method is a function defined inside a class.
17. Pydantic adds validation on top of structured Python models.
18. An FDE should identify the actual failure layer before blaming the AI model.

---

# B2D Cloud AI Knowledge Assistant Progress

The application now supports:

```text
GET /health
GET /documents
POST /ask
```

Current architecture:

```text
Student
  ↓
question
  ↓
POST /ask
  ↓
FastAPI
  ↓
Pydantic validation
  ↓
placeholder answer
```

The next major step is:

```text
question
  ↓
retrieve relevant school documents
  ↓
context
  ↓
LLM
  ↓
answer
```

That will begin the first real step toward RAG.

---

# Day 5 Completion Checkpoint

## Completed

- [x] Virtual environment created and activated
- [x] FastAPI running from project environment
- [x] `GET /health` verified
- [x] `GET /documents` verified
- [x] `POST /ask` created
- [x] Valid POST request returned `200`
- [x] Wrong field request returned `422`
- [x] Empty object returned `422`
- [x] Empty string returned `200`
- [x] Pydantic schema understood
- [x] Python class created
- [x] Object created
- [x] Attributes added
- [x] `__init__` used
- [x] `self` practiced
- [x] `to_dict()` method created
- [x] Object converted into dictionary

## Next Step

Begin learning document retrieval for the B2D Cloud AI Knowledge Assistant so the `/ask` endpoint can eventually answer questions using actual school documents instead of a placeholder response.