import json
import re

def clean_ipc_section(section):
    # Normalizes IPC section strings.
    # Example: 'Section 302 I.P.C' -> 'Section 302 IPC'
    # Standardize to "Section {Code} IPC"
    m = re.search(r'(\d+[A-Z\-/]*\d*[A-Z]*)', section)
    if m:
        code = m.group(1).strip('-/ ').upper()
        return f"Section {code} IPC"
    return section

def extract_ipc_from_text(text):
    if not text:
        return []
        
    ipc_pattern = r'I\.?P\.?C|Indian\s+Penal\s+Code'
    section_prefix = r'(?:Sections?|u/s|u/ss|u\.s\.|U/s|U\.S\.|under\s+Sections?|under\s+)'
    
    found = set()
    # Normalize space for searching
    search_text = re.sub(r'\s+', ' ', text)

    # 1. Matches with IPC nearby (High Confidence)
    pattern1 = rf'{section_prefix}\s+([A-Z\d,\s/&\-and]+?)(?:\s+of\s+)?(?:\s+the\s+)?(?:{ipc_pattern})'
    for m in re.finditer(pattern1, search_text, re.IGNORECASE):
        raw_sections = m.group(1)
        potential_sections = re.findall(r'\b\d+[A-Z\-/]*\d*[A-Z]*\b', raw_sections)
        for s in potential_sections:
            s = s.strip('-/ ')
            if s:
                if '/' in s:
                    for part in s.split('/'):
                        p = part.strip().upper()
                        if p: found.add(f"Section {p} IPC")
                else:
                    found.add(f"Section {s.upper()} IPC")

    # 2. Matches like "IPC Section 302" (High Confidence)
    pattern2 = rf'(?:{ipc_pattern})\s+{section_prefix}?\s*([A-Z\d,\s/&\-and]+)'
    for m in re.finditer(pattern2, search_text, re.IGNORECASE):
        raw_sections = m.group(1)
        potential_sections = re.findall(r'\b\d+[A-Z\-/]*\d*[A-Z]*\b', raw_sections)
        for s in potential_sections[:5]:
            s = s.strip('-/ ')
            if s:
                if '/' in s:
                    for part in s.split('/'):
                        p = part.strip().upper()
                        if p: found.add(f"Section {p} IPC")
                else:
                    found.add(f"Section {s.upper()} IPC")
                    
    # 3. extraction with range filtering (Medium Confidence)
    # IPC sections are between 1 and 511.
    pattern3 = rf'({section_prefix})\s*([A-Z\d,\s/&\-and]+)'
    for m in re.finditer(pattern3, search_text, re.IGNORECASE):
        raw_sections = m.group(2)
        # Limit to the first part to avoid long matches
        first_part = raw_sections.split(' ')[0].strip(',')
        potential_sections = re.findall(r'\b\d+[A-Z\-/]*\d*[A-Z]*\b', first_part)
        for s in potential_sections:
            s = s.strip('-/ ')
            if s:
                # Check if it looks like a valid IPC section
                num_m = re.search(r'\d+', s)
                if num_m:
                    num = int(num_m.group())
                    if 1 <= num <= 511:
                        if '/' in s:
                            for part in s.split('/'):
                                p = part.strip().upper()
                                if p: found.add(f"Section {p} IPC")
                        else:
                            found.add(f"Section {s.upper()} IPC")
                
    return list(found)

def clean_judgment(text):
    # Cleans judgment text: removes boilerplate, normalizes line wraps and whitespace.
    if not text:
        return ""
        
    # Remove "J U D G M E N T" variations and repetitive markers
    text = re.sub(r'J\s*U\s*D\s*G\s*M\s*E\s*N\s*T', '', text, flags=re.IGNORECASE)
    
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        l = line.strip()
        # Skip header/footer lines
        if re.match(r'^\d{1,2}/\d{1,2}/\d{2,4}$', l): continue
        if l.upper().startswith('BENCH:'): continue
        if l.upper() == 'JUDGMENT:': continue
        if l.upper() == 'ORDER:': continue
        # Skip lines that are just "JUDGMENT" after removing spaces
        if re.match(r'^[JUDGMENT\s]*$', l, re.IGNORECASE) and len(l.replace(' ', '')) == 8: continue
        
        cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # Normalize spaces
    text = re.sub(r' +', ' ', text)
    
    # Identify hard wraps: a newline NOT preceded by sentence-ending punctuation is likely a wrap.
    text = re.sub(r'([^\.\!\?\:\;])\n', r'\1 ', text)
    
    # Replace remaining newlines with spaces for a single clean paragraph
    text = text.replace('\n', ' ')
    
    # Final normalization of all white space
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def clean_item(item):
    # Cleans title, judgment, and ipc_sections in a case item.
    # Clean Title

    title = item.get("title", "")
    title = re.sub(r'\s+', ' ', title).strip()

    # Remove dates like "on 24 November, 2006" at the end of titles

    title = re.sub(r'\s+on\s+\d+.*?$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s+on$', '', title, flags=re.IGNORECASE)
    title = re.sub(r',$', '', title).strip()
    item["title"] = title
    
    # Clean Judgment
    item["judgment"] = clean_judgment(item.get("judgment", ""))
    
    # Clean and Extract IPC Sections
    ipc_sections = item.get("ipc_sections", [])
    # Re-extract from (cleaned) judgment text
    ipc_sections.extend(extract_ipc_from_text(item["judgment"]))
    
    cleaned_sections = set()
    for section in ipc_sections:
        normalized = clean_ipc_section(section)
        if normalized:
            cleaned_sections.add(normalized)
            
    item["ipc_sections"] = sorted(list(cleaned_sections))
    
    return item

def main():
    input_file = "criminal_cases.json"
    output_file = "Cleaned_criminal_cases.json"
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {input_file}: {e}")
        return

    print(f"Processing {len(data)} items...")
    
    # Apply cleaning to each item
    cleaned_data = [clean_item(item) for item in data]
    
    # remove duplicate items
    unique_items = []
    seen = set()
    for item in cleaned_data:
        # Use first 200 chars for identification
        identifier = (item["title"].lower(), item["judgment"][:200].lower())
        if identifier not in seen:
            unique_items.append(item)
            seen.add(identifier)
    
    # Write the cleaned data back
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(unique_items, f, indent=4, ensure_ascii=False)
    
    print(f"Cleaned JSON saved to {output_file}.")
    print(f"Original items: {len(data)}")
    print(f"Unique items after cleaning: {len(unique_items)}")

if __name__ == "__main__":
    main()
