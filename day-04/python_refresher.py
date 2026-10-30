```python
def health_check():
    return {
        "status": "ok"
    }


# Reflection Questions
#
# 1. What is the function name?
#    health_check is the function name.
#
# 2. Does the function take any arguments?
#    It doesn't currently take any arguments.
#
# 3. What data type does it return?
#    Dictionary.
#
# 4. What key exists in the returned dictionary?
#    "status"
#
# 5. What value belongs to that key?
#    "ok"
#
# 6. What does return do?
#    return sends a value back from a function to the code that called it.
#
# 7. What is the difference between a list and a dictionary?
#    A list stores multiple items using [].
#    A dictionary stores key-value pairs using {}.
#
# 8. Can a dictionary contain a list?
#    Yes. A dictionary value can be a list.
#
# 9. Why would an API return a dictionary?
#    A dictionary helps organize related information under meaningful keys.
#
# 10. How does FastAPI turn Python data into JSON?
#     FastAPI automatically serializes supported Python data,
#     such as dictionaries and lists, into JSON before sending
#     the HTTP response.
#
# 11. Why is get_documents() still a normal Python function
#     even when FastAPI uses it as an endpoint?
#     It is still defined using normal Python function syntax.
#     FastAPI's route decorator connects that function to an
#     HTTP endpoint and calls it when a matching request arrives.


def get_system_status():
    return {
        "service_name": "b2d-knowledge-api",
        "status": "ok",
        "port": 8000
    }


print(get_system_status())


documents = [
    "attendance-policy.txt",
    "student-handbook.txt",
    "career-guide.txt"
]


def get_documents():
    return {
        "documents": documents,
        "count": len(documents)
    }


print(get_documents())
```