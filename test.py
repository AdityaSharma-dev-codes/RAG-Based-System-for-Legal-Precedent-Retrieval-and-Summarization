import json

with open("criminal_cases.json", "r") as f1:
    data1 = json.load(f1)

with open("Cleaned_criminal_cases.json", "r") as f2:
    data2 = json.load(f2)

def check_missing(data):
    # Checking and counting the number of missing data in each section of the JSON file
    count = [0, 0, 0]

    for t in data:
        if t["title"] == "":
            count[0] += 1

    for judge in data:
        if judge["judgment"] == "":
            count[1] += 1

    for ipc in data:
        if ipc["ipc_sections"] == [] or ipc["ipc_sections"] == ["Unknown"]:
            count[2] += 1
    return count

def check_word_count(data):
    # Checking the average, min and max number of words in "judgment" section
    word_counts = []
    words_final = [0,0,0]
    for item in data:
        judgment = item.get("judgment", "")
        if judgment:
            words = judgment.split()
            word_counts.append(len(words))
    
    words_final[0] = sum(word_counts) / len(word_counts)
    words_final[1] = min(word_counts)
    words_final[2] = max(word_counts)
    
    return words_final

print(f"Number of missing Title, Judgment, IPC Sections in criminal_cases.json: {check_missing(data1)}")
print(f"Criminal_cases.json - Judgment Word Count: {check_word_count(data1)}")

print(f"Number of missing Title, Judgment, IPC Sections in Cleaned_criminal_cases.json: {check_missing(data2)}")
print(f"Cleaned_criminal_cases.json - Judgment Word Count: {check_word_count(data2)}")
