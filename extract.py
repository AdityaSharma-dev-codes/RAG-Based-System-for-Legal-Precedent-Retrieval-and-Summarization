import os
import fitz
import json
import re

count = 0
base_dir = "DataSet"

def clean_text(txt):
    # Remove form feed characters (\f)
    txt = txt.replace('\f', '')

    # Remove URLs
    txt = re.sub(r'http\S+', '', txt)

    # Remove excessive newlines
    txt = re.sub(r'\n+', '\n', txt)

    # Remove citations (AIR, SCC, etc.)
    txt = re.sub(r'\bAIR\b.*?\n', '', txt)
    txt = re.sub(r'\b\d{4}.*?SCC.*?\n', '', txt)

    # Remove "Indian Kanoon" lines
    txt = re.sub(r'Indian Kanoon.*?\n', '', txt)

    # Remove page numbers
    txt = re.sub(r'\n\d+\n', '\n', txt)

    # Remove extra spaces
    txt = re.sub(r' +', ' ', txt)

    return txt.strip()


def extract_structure(txt):
    data = {}

    # Case Title (first line)
    lines = txt.split("\n")
    data["title"] = lines[0] if lines else ""

    # Extract judgment section
    # Search for JUDGMENT or ORDER, optionally followed by a colon and whitespace
    judgment_match = re.search(r'\b(?:JUDGMENT|ORDER)\b[:\s]*(.*)', txt, re.DOTALL | re.IGNORECASE)
    data["judgment"] = judgment_match.group(1).strip() if judgment_match else txt[:2000]

    # Extract IPC Sections
    ipc_sections = re.findall(r'Section\s+\d+\s+I\.?P\.?C', txt, re.IGNORECASE)
    data["ipc_sections"] = list(set(ipc_sections))

    return data


def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    txt = ""
    for page in doc:
        txt += page.get_text()
    return txt

def is_criminal_case(txt):
    txt = txt.lower()

    if "ipc" in txt:
        return True
    if "state vs" in txt:
        return True
    if "accused" in txt and "conviction" in txt:
        return True

    return False

results = []
for year in os.listdir(base_dir):
    y_path = os.path.join(base_dir, year)

    if os.path.isdir(y_path):
        for file in os.listdir(y_path):
            pdf_path = os.path.join(y_path, file)

            try:
                text = extract_text(pdf_path)

                if is_criminal_case(text):
                    print(f"file {pdf_path} from {year} is about a criminal case")

                    clean = clean_text(text)
                    structured = extract_structure(clean)

                    results.append(structured)
                    count += 1
                else:
                    # run the next 2 lines only for the first run
                    os.remove(pdf_path)
                    print(f"deleted file {pdf_path} from {year}")
                    pass
                
            except Exception as e:
                print(f"Error reading file {file}: {e}")

# Write the final results as a pretty-printed JSON array
with open("criminal_cases.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print(f"Number of Files of criminal cases: {count}")