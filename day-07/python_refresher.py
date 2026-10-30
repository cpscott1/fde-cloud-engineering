expected_source = None
actual_source = None

is_correct = actual_source == expected_source

print(is_correct)

results = [
    True,
    True,
    False,
    True
]

passed = 0

for result in results:
    if result:
        passed += 1

print(passed)
    
passed = 3
total = 4

accuracy = passed / total * 100

print(accuracy)