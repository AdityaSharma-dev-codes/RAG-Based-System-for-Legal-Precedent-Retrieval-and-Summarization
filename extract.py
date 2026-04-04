import os
import fitz
import json

count = 0
base_dir = "DataSet"

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

                    data = {
                        "file": file,
                        "year": year,
                        "text": text
                    }

                    with open("criminal_cases.json", "a", encoding="utf-8") as f:
                        json.dump(data, f)
                        f.write("\n")

                    count += 1
                else:
                    os.remove(pdf_path)
                    print(f"deleted file {pdf_path} from {year}")

            except Exception as e:
                print(f"Error reading file{file}: {e}")

print(f"Number of Files of criminal cases: {count}")