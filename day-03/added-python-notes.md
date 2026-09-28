You're definitely on the right track. **#1 and #4 are correct**, while #2 and #3 need small corrections. The main concept to strengthen is the difference between a **Python dictionary** and **JSON**, and how nested data structures are accessed.

# Day 3 Python Notes — Lists, Dictionaries, and Nested Data

## Practice Prompt Review

Given this Python code:

```python
endpoints = [
    {
        "name": "primary-policy",
        "url": "http://127.0.0.1:8000/attendance-policy.txt"
    },
    {
        "name": "missing-policy",
        "url": "http://127.0.0.1:8000/missing-policy.txt"
    },
    {
        "name": "alternate-policy",
        "url": "http://127.0.0.1:8001/attendance-policy.txt"
    }
]
```

---

## 1. What Python data type is `endpoints`?

### My original answer

> Maybe it's a list.

### Result

**Correct.**

`endpoints` is a Python **list**.

We can tell because the outer structure uses square brackets:

```python
endpoints = [
    ...
]
```

A simple way to remember this is:

```text
[] → list
{} → dictionary
```

A list is useful when I want to store multiple items together.

In this example, I have three endpoints stored in one list.

```text
endpoints
   ↓
┌──────────────────────────┐
│ endpoint 0               │
│ endpoint 1               │
│ endpoint 2               │
└──────────────────────────┘
```

Python lists start counting at `0`.

Therefore:

```python
endpoints[0]
```

means:

> Give me the first item in the `endpoints` list.

---

## 2. What data type is each item inside `endpoints`?

### My original answer

> JSON data.

### Correction

Each item is a Python **dictionary**, also called a `dict`.

For example:

```python
{
    "name": "primary-policy",
    "url": "http://127.0.0.1:8000/attendance-policy.txt"
}
```

This is a Python dictionary.

A dictionary stores information using **key-value pairs**.

For example:

```text
KEY        VALUE

name   →   primary-policy

url    →   http://127.0.0.1:8000/attendance-policy.txt
```

So I can access values using their keys:

```python
endpoint["name"]
```

or:

```python
endpoint["url"]
```

### Dictionary vs JSON

Python dictionaries and JSON often look very similar, which is why they can be confusing.

Python:

```python
student = {
    "name": "Alex",
    "grade": 10
}
```

JSON:

```json
{
    "name": "Alex",
    "grade": 10
}
```

They look almost identical, but they are not the same thing.

A **dictionary is a Python data structure being used by my Python program.**

**JSON is a text-based data format commonly used to exchange data between systems.**

For example, later the B2D Cloud AI Knowledge Assistant might work like this:

```text
Frontend
   ↓
JSON
   ↓
FastAPI
   ↓
Python dictionary
   ↓
Python code
```

This distinction will become important when working with APIs.

---

## 3. How would I access the first endpoint's URL?

### My original answer

```python
print(endpoint[0])
```

### Correction

I was close because I correctly remembered that `[0]` accesses the first item of a list.

However, the variable is called:

```python
endpoints
```

not:

```python
endpoint
```

First I could access the first endpoint:

```python
endpoints[0]
```

That gives me the entire first dictionary:

```python
{
    "name": "primary-policy",
    "url": "http://127.0.0.1:8000/attendance-policy.txt"
}
```

But the question asks specifically for its **URL**.

Therefore I need another step.

```python
endpoints[0]["url"]
```

This can be read from left to right:

```text
endpoints
    ↓
[0]
    ↓
first dictionary
    ↓
["url"]
    ↓
value stored under the url key
```

So:

```python
print(endpoints[0]["url"])
```

would print:

```text
http://127.0.0.1:8000/attendance-policy.txt
```

### Mental model

When I see:

```python
endpoints[0]["url"]
```

I can think:

> Go into `endpoints` → get the first item → get its `url`.

This is called accessing **nested data**.

---

## 4. How would I loop through every endpoint?

### My original answer

> Doing a for loop.

### Result

**Correct.**

A `for` loop is appropriate because I want Python to perform an action for every item in the list.

For example:

```python
for endpoint in endpoints:
    print(endpoint)
```

Python essentially does this:

```text
endpoints

   ↓

FIRST LOOP

endpoint =
{
    "name": "primary-policy",
    "url": "..."
}

   ↓

SECOND LOOP

endpoint =
{
    "name": "missing-policy",
    "url": "..."
}

   ↓

THIRD LOOP

endpoint =
{
    "name": "alternate-policy",
    "url": "..."
}
```

Inside the loop, `endpoint` represents the current dictionary.

Therefore I could access:

```python
endpoint["name"]
```

and:

```python
endpoint["url"]
```

For example:

```python
for endpoint in endpoints:
    print(endpoint["name"])
    print(endpoint["url"])
```

---

# Important Python Mental Model

The data structure can be visualized as:

```text
endpoints                       LIST
│
├── [0]                         DICTIONARY
│    ├── "name"
│    └── "url"
│
├── [1]                         DICTIONARY
│    ├── "name"
│    └── "url"
│
└── [2]                         DICTIONARY
     ├── "name"
     └── "url"
```

Therefore:

```python
endpoints[0]
```

means:

```text
Give me the first dictionary.
```

While:

```python
endpoints[0]["url"]
```

means:

```text
Give me the first dictionary
        ↓
then give me its URL.
```

---

# Why This Matters for FDE Work

Nested lists and dictionaries appear constantly when working with APIs, cloud services, and AI applications.

For example, an AI application might work with data shaped like:

```python
students = [
    {
        "name": "Alex",
        "grade": 10,
        "question": "What is the attendance policy?"
    },
    {
        "name": "Jordan",
        "grade": 11,
        "question": "When does school start?"
    }
]
```

Or our application might keep track of services:

```python
services = [
    {
        "name": "knowledge-api",
        "url": "http://127.0.0.1:8000",
        "healthy": True
    }
]
```

Understanding:

```text
lists
+
dictionaries
+
loops
```

will make it much easier to understand APIs, JSON, FastAPI, RAG results, configuration files, and health checks later.

# Day 3 Key Takeaway

```text
[] = List
     ↓
contains multiple items

{} = Dictionary
     ↓
contains key-value pairs

[0] = First list item

["url"] = Value associated with the "url" key

for = Repeat something for each item
```

One especially important correction is **#2**. Calling it JSON is a very reasonable guess because it looks almost identical, but in the code you're currently writing, it's a **Python dictionary**. When we get to FastAPI, you'll see exactly how Python dictionaries get converted to/from JSON, which should make that distinction click.

For **#3**, you had the harder part right: you remembered `[0]` means the first item. Now we're just adding the idea that once you have that dictionary, `["url"]` selects the value you want.