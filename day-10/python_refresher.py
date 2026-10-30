from pathlib import Path

file = Path("app.py")
print(file.exists())

missing_file = Path("missing-text.txt")
print(missing_file.exists())

required_files = [
    "app.py",
    "retrieval.py",
    "requirements.txt",
    "Dockerfile",
    "missing-text.txt"
]

missing_files = []

for item in required_files:
    item_path = Path(item)

    # if item_path.exists() == False:
    if not item_path.exists():
        missing_files.append(item)
    print(item,item_path.exists())

print(missing_files)

def find_missing_files(files):
    missing = []
    for item in files:
        missing_path = Path(item)

        if not missing_path.exists():
            missing.append(item)

    return missing

result = find_missing_files(required_files)

print("Missing files:", result)

test_files = [
    "app.py",
    "another-missing-file.txt"
]

print("Second test:", find_missing_files(test_files))

def ready_to_build(files):
    for item in files:
        check_item = Path(item)
        
        if not check_item.exists():
            return False 
            
    return True

actual_files = [
    "app.py",
    "retrieval.py",
    "requirements.txt",
    "Dockerfile"
]

print("Ready with real files:", ready_to_build(actual_files))

print("Ready with missing file:", ready_to_build(test_files))

