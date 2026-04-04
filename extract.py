import os
import fitz
import json
import re

count = 0
base_dir = "DataSet"

def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Remove excessive newlines
    text = re.sub(r'\n+', '\n', text)

    # Remove citations (AIR, SCC etc.)
    text = re.sub(r'\bAIR\b.*?\n', '', text)
    text = re.sub(r'\b\d{4}.*?SCC.*?\n', '', text)

    # Remove "Indian Kanoon" lines
    text = re.sub(r'Indian Kanoon.*?\n', '', text)

    # Remove page numbers
    text = re.sub(r'\n\d+\n', '\n', text)

    # Remove extra spaces
    text = re.sub(r' +', ' ', text)

    return text.strip()


def extract_structure(text):
    data = {}

    # Case Title (first line)
    lines = text.split("\n")
    data["title"] = lines[0] if lines else ""

    # Extract judgment section
    judgment_match = re.search(r'JUDGMENT:(.*)', text, re.DOTALL)
    data["judgment"] = judgment_match.group(1).strip() if judgment_match else text[:2000]

    # Extract IPC Sections
    ipc_sections = re.findall(r'Section\s+\d+\s+I\.?P\.?C', text)
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

for year in os.listdir(base_dir):
    y_path = os.path.join(base_dir, year)

    if os.path.isdir(y_path):
        for file in os.listdir(y_path):
            pdf_path = os.path.join(y_path, file)

            try:
                text = extract_text(pdf_path)

                if is_criminal_case(text):
                    print(f"{year} criminal")

                    clean = clean_text(text)
                    structured = extract_structure(clean)

                    with open("criminal_cases.json", "a", encoding="utf-8") as f:
                        json.dump(structured, f)
                        f.write("\n")

                    count += 1
                else:
                    pass
                    # os.remove(pdf_path)
                    # print(f"deleted file {pdf_path} from {year}")

            except Exception as e:
                print(f"Error reading file{file}: {e}")

print(f"Number of Files of criminal cases: {count}")