import json
import faiss
from sentence_transformers import SentenceTransformer

def main():
    # File paths
    input_file = "Chunked_criminal_cases.json"
    index_file = "vector_index.faiss"
    
    # 1. Load Chunks
    print(f"Loading chunks from {input_file}...")
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    chunks = [item["chunk"] for item in data]
    print(f"Total chunks: {len(chunks)}")

    # 2. Initialize SBERT Model
    print("Initializing SBERT model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 3. Generate Embeddings
    print("Generating embeddings (this may take a while)...")
    # Using encode with show_progress_bar=True and a reasonable batch size
    embeddings = model.encode(chunks, batch_size=64, show_progress_bar=True, convert_to_numpy=True)
    
    # 4. Store in FAISS
    print("Building FAISS index (Cosine Similarity)...")
    dimension = embeddings.shape[1]
    
    # Normalize embeddings for cosine similarity
    embeddings = embeddings.astype('float32')
    faiss.normalize_L2(embeddings)
    
    # Use Inner Product index with normalized vectors to get cosine similarity
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    
    # 5. Save Index
    print(f"Saving FAISS index to {index_file}...")
    faiss.write_index(index, index_file)
    
    print("Vectorization complete.")

if __name__ == "__main__":
    main()
