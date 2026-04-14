import json

with open("criminal_cases.json", "r") as f1:
    data1 = json.load(f1)

with open("Cleaned_criminal_cases.json", "r") as f2:
    data2 = json.load(f2)

def check(data):
    # Checking and counting the number of missing data in each section of the JSON file
    count = [0, 0, 0]

    for t in data:
        if t["title"] == "":
            count[0] += 1

    for judge in data:
        if judge["judgment"] == "":
            count[1] += 1

    for ipc in data:
        if ipc["ipc_sections"] == []:
            count[2] += 1
    return count

print(f"Number of missing Title, Judgment, IPC Sections in criminal_cases.json: {check(data1)}")
print(f"Number of missing Title, Judgment, IPC Sections in Cleaned_criminal_cases.json: {check(data2)}")
