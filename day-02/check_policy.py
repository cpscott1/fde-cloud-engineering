try:
    with open("policy.txt", encoding="utf-8") as f:
        read_data = f.read()

    print(read_data)
    words = read_data.split()
    word_count = len(words)
    print("Word count:", word_count)

except FileNotFoundError:
    print("Could not find the policy file.")
