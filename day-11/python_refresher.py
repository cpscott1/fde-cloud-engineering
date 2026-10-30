documents = ["attendance-policy.txt", "career-guide.txt", "student-handbook.txt"]

missing_documents = []

print("Available documents:", len(documents))
print("Missing documents:", len(missing_documents))

def count_documents(files):
    return len(files)

print("Function count (available):", count_documents(documents))
print("Function count (missing):", count_documents(missing_documents))

ready_result = {
    "status_code": 200,
    "status": "ready",
    "document_count": 3
}

print(ready_result)
print(ready_result["status"])

def build_readiness_result(files):
    document_count = count_documents(files)

    if document_count == 0:
        return {
            "status_code": 503,
            "status": "not_ready",
            "document_count": document_count
        }
    else:
        return {
            "status_code": 200,
            "status": "ready",
            "document_count": document_count
        }


print("Ready result:", build_readiness_result(documents))
print("Not ready result:", build_readiness_result(missing_documents))

ready_result = build_readiness_result(documents)
assert ready_result["status_code"] == 200, "Ready status code should be 200"

print("First assertion passed")

not_ready_result = build_readiness_result(missing_documents)
assert not_ready_result["status_code"] == 503, "Not-ready status code is incorrect"

print("Both assertions passed")

assert ready_result["status"] == "ready", "Ready status should be ready"

assert not_ready_result["status"] == "not_ready", "Not-ready status is incorrect"

print("Both status assertion passed")

assert ready_result["document_count"] == 3, "Ready document is incorrect"

assert not_ready_result["document_count"] == 0, "Not-ready document count is incorrect"

print("All six readiness assertions passed")