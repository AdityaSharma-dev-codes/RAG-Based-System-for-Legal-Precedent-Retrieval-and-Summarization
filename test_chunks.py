import json

with open("Chunked_criminal_cases.json", "r", encoding="utf-8") as f1:
    data1 = json.load(f1)

def word_count_in_chunk(data):
    count_above_300 = 0
    count_above_400 = 0
    total_words = 0
    total_chunks = 0
    max_words = 0
    min_words = float('inf')

    for case in data:
        chunks = case.get("judgment_chunks", [])
        for chunk in chunks:
            words = chunk.split()
            word_count = len(words)
            
            total_chunks += 1
            total_words += word_count
            
            if word_count > 300:
                count_above_300 += 1
            if word_count > 400:
                count_above_400 += 1
                
            if word_count > max_words:
                max_words = word_count
            if word_count < min_words:
                min_words = word_count

    avg_words = total_words / total_chunks if total_chunks > 0 else 0
    min_words = min_words if total_chunks > 0 else 0

    print(f"Number of chunks with words > 300: {count_above_300}")
    print(f"Average number of words in each chunk: {avg_words:.2f}")
    print(f"Maximum number of words in a chunk: {max_words}")
    print(f"Minimum number of words in a chunk: {min_words}")


word_count_in_chunk(data1)