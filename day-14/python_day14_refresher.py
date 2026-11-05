from pathlib import Path

knowledge_dir = Path("district-a/knowledge")

print("Path:", knowledge_dir)
print("Exists:", knowledge_dir.exists())
print("Is directory:", knowledge_dir.is_dir())

districts = [
    Path("district-a/knowledge"),
    Path("district-b/knowledge")
]

for district in districts:
    print(district)
    print("Exists:", district.exists())
    print("Is directory:", district.is_dir())

def find_policy_files(directory): 
    results = list(directory.glob("*.txt"))
    sorted_results = sorted(results)
    return sorted_results

policy_files = find_policy_files(knowledge_dir)
print("Policy files:", policy_files)

print("District A files:", find_policy_files(districts[0]))
print("District B files:", find_policy_files(districts[1]))

def count_documents(directory):
    count_files = len(find_policy_files(directory))
    return count_files

print("District A count:", count_documents(districts[0]))
print("District B count:", count_documents(districts[1]))

def summarize_knowledge_base(district_name, directory):
    document_exists = directory.exists()
    document_count = count_documents(directory)
    district_record = {
        "district": district_name,
        "directory": directory,
        "exists": document_exists,
        "document_count": document_count
    }
    return district_record

print("District A summary:", summarize_knowledge_base("District A", districts[0]))
print("District B summary:", summarize_knowledge_base("District B", districts[1]))