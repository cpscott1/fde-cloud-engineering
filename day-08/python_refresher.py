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

words = {
    "cellphones": "phone",
    "phones": "phone"
}

print(words.get("cellphones"))

def normalized_word(word):
    return words.get(word, word)

print(normalized_word("cellphones"))
print(normalized_word("attendance"))

question_words = [
    "are",
    "cellphones",
    "allowed",
    "during",
    "class"
]

for word in question_words:
    print(normalized_word(word))

normalized_words = []

for word in question_words:
    normalized_words.append(normalized_word(word))

print(normalized_words)