import os
import fitz

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

for y in os.listdir(base_dir):
    y_path = os.path.join(base_dir, y)

    if os.path.isdir(y_path):
        for file in os.listdir(y_path):
            pdf_path = os.path.join(y_path, file)

            try:
                text = extract_text(pdf_path)

                if is_criminal_case(text):
                    print(f"{y} criminal")
                    count += 1
                else:
                    print(f"{y} no")

            except Exception as e:
                print(f"Error reading file{file}: {e}")

print(count)