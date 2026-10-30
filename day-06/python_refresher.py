document = {
    "source": "attendance-policy.txt",
    "score": 2
}

print(document["source"])
print(document["score"])

def build_result(source, score):
    result = {
        "source": source,
        "score": score
    }

    return result

answer = build_result("student-handbook.txt", 3)

print(answer)

results = [
    {"source": "attendance-policy.txt", "score": 0},
    {"source": "student-handbook.txt", "score": 0},
    {"source": "career-guide.txt", "score": 0},
]

for result in results:
    print(result["source"])

best_score = 0
best_result = None

for result in results:
    if result["score"] > best_score:
        best_score = result["score"]
        best_result = result

print(best_result)