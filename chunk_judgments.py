import json
import spacy
import os

def chunk_text(text, nlp, max_words=250, overlap=50):
    if not text:
        return []

    doc = nlp(text)
    chunks = []
    current_chunk = []
    current_word_count = 0
    overlap_only = False
    
    for sent in doc.sents:
        sent_text = sent.text.strip()
        if not sent_text:
            continue
        
        sent_words = sent_text.split()
        sent_word_count = len(sent_words)
        
        if current_word_count + sent_word_count > max_words:
            if current_chunk:
                chunk_str = " ".join(current_chunk)
                chunks.append(chunk_str)
                
                # Add overlap
                overlap_words = " ".join(chunk_str.split()[-overlap:])
                current_chunk = [overlap_words]
                current_word_count = len(overlap_words.split())
                overlap_only = True
            
            # If a single sentence is longer than max_words, split it by words
            if sent_word_count > max_words:
                for i in range(0, sent_word_count, max_words - overlap):
                    chunk = " ".join(sent_words[i:i + max_words])
                    chunks.append(chunk)
                
                # Prepare overlap for the next sentence
                overlap_words = " ".join(sent_words[-overlap:])
                current_chunk = [overlap_words]
                current_word_count = len(overlap_words.split())
                overlap_only = True
                continue
        
        current_chunk.append(sent_text)
        current_word_count += sent_word_count
        overlap_only = False
        
    if current_chunk and not overlap_only:
        chunks.append(" ".join(current_chunk))

    return chunks

def main():
    input_file = "Cleaned_criminal_cases.json"
    output_file = "Chunked_criminal_cases.json"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print("Loading SpaCy model...")
    # Using a blank English model with just the sentencizer
    nlp = spacy.blank("en")
    nlp.add_pipe("sentencizer")
    # Increase max_length to handle very long judgments
    nlp.max_length = 3000000 
    
    print(f"Loading {input_file}...")
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    chunked_data = []
    
    total_cases = len(data)
    print(f"Processing {total_cases} cases...")
    
    for i, case in enumerate(data):
        judgment = case.get("judgment", "")
        if judgment:
            chunks = chunk_text(judgment, nlp, max_words=250, overlap=50)
            for chunk in chunks:
                if len(chunk.split()) < 30:
                    continue
                chunked_data.append({
                    "title": case.get("title", "Unknown"),
                    "ipc_sections": case.get("ipc_sections", []),
                    "chunk": chunk,
                })
            
        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{total_cases} cases...")

    print(f"Saving to {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunked_data, f, indent=4)

    print("Done!")

if __name__ == "__main__":
    main()
