import json

with open("Chunked_criminal_cases.json", "r", encoding="utf-8") as f1:
    data1 = json.load(f1)

def word_count_in_chunk(data):
    count_above_250 = 0
    count_below_30 = 0
    count_below_50 = 0
    total_words = 0
    total_chunks = 0
    max_words = 0
    min_words = float('inf')

    for chunk_obj in data:
        chunk = chunk_obj.get("chunk", "")
        if not chunk:
            continue
        words = chunk.split()
        word_count = len(words)
        
        total_chunks += 1
        total_words += word_count
        
        if word_count > 250:
            count_above_250 += 1
        if word_count < 30:
            count_below_30 += 1
        if word_count < 50:
            count_below_50 += 1
        if word_count > max_words:
            max_words = word_count
        if word_count < min_words:
            min_words = word_count

    avg_words = total_words / total_chunks if total_chunks > 0 else 0
    min_words = min_words if total_chunks > 0 else 0

    print(f"Total chunks: {total_chunks}")
    print(f"Number of chunks with words > 250: {count_above_250}")
    print(f"Number of chunks with words < 30: {count_below_30}")
    print(f"Number of chunks with words < 50: {count_below_50}")
    print(f"Average number of words in each chunk: {avg_words:.2f}")
    print(f"Maximum number of words in a chunk: {max_words}")
    print(f"Minimum number of words in a chunk: {min_words}")


word_count_in_chunk(data1)