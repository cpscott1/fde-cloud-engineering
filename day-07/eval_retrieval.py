import logging 
from retrieval import search_documents

logging.basicConfig(level=logging.INFO)

test_cases = [
    {
        "question": "What is the attendance policy?",
        "expected_source": "attendance-policy.txt"
    },
    {
        "question": "Can students use phones during class?",
        "expected_source": "student-handbook.txt"
    },
    {
        "question": "What is for lunch tomorrow?",
        "expected_source": None
    },
    {
        "question": "Are cellphones allowed?",
        "expected_source": "student-handbook.txt"
    }
] 

passed = 0

for test_case in test_cases:
    result = search_documents(test_case["question"])

    expected_source = test_case["expected_source"]
    actual_source = result["source"]

    is_correct = actual_source == expected_source


    print(test_case["question"])
    print(expected_source)
    print(result)
    print(is_correct)

    if is_correct:
        passed += 1
        print("PASS")
    else: 
        print("FAIL")

total = len(test_cases)
accuracy = (passed / total) * 100

print("Passed:", passed)
print("Total:", total)
print("Accuracy:", accuracy)