import json
import faiss
import os
import google.generativeai as genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load environment variables from .env file
load_dotenv()

class LegalQuerySystem:
    def __init__(self, index_path="vector_index.faiss", metadata_path="Chunked_criminal_cases.json", 
                 model_name='all-MiniLM-L6-v2', api_key=None):
        print("Loading SBERT model...")
        self.model = SentenceTransformer(model_name)
        
        print(f"Loading FAISS index from {index_path}...")
        self.index = faiss.read_index(index_path)
        
        print(f"Loading metadata from {metadata_path}...")
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
            
        # Configure Gemini LLM
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.llm_available = True
        else:
            print("Warning: GOOGLE_API_KEY not found. RAG functionality will be limited.")
            self.llm_available = False
            
    def search(self, query, k=5, threshold=0.5):
        # 1. Generate query embedding
        query_vector = self.model.encode([query]).astype('float32')
        
        # Normalize query vector for cosine similarity
        faiss.normalize_L2(query_vector)
        
        # 2. Search FAISS index
        scores, indices = self.index.search(query_vector, k)
        
        # 3. Retrieve metadata
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:
                score = float(scores[0][i])
                # 4. Basic filtering based on threshold
                if score < threshold:
                    continue
                    
                result = self.metadata[idx].copy()
                result['score'] = score
                results.append(result)
        
        return results

    def generate_answer(self, query, results):
        """
        Generates an answer using the LLM based on retrieved chunks (RAG).
        """
        if not self.llm_available:
            return "Error: LLM not configured. Please provide a GOOGLE_API_KEY."
            
        if not results:
            return "No relevant legal context found to answer the query."
        
        # 1. Combine retrieved chunks into context
        context = "\n\n".join([f"--- Context Chunk {i+1} ---\n{res['chunk']}" for i, res in enumerate(results)])
        
        # 2. Construct prompt
        prompt = f"""
Based on the following legal context:
{context}

Answer the following query accurately based ONLY on the provided legal context. 
If the information is not present, state that the context does not provide a direct answer.

Query: {query}

Answer:"""
        
        # 3. Send to LLM
        try:
            model = genai.GenerativeModel('gemini-3-flash-preview')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error during LLM generation: {str(e)}"

def main():
    # Example usage
    # Note: Ensure vector_index.faiss exists before running this example
    import os
    index_path = "vector_index.faiss"
    
    # Check if index exists, if not use the test one if available
    if not os.path.exists(index_path):
        if os.path.exists("test_index.faiss"):
            index_path = "test_index.faiss"
            metadata_path = "test_subset.json"
        else:
            print("Error: vector_index.faiss not found. Run vectorize.py first.")
            return
    else:
        metadata_path = "Chunked_criminal_cases.json"

    qs = LegalQuerySystem(index_path=index_path, metadata_path=metadata_path)
    
    query = "What is the punishment for murder under IPC 302?"
    print(f"\nQuery: {query}")
    results = qs.search(query, k=3, threshold=0.4)
    
    # 1. Show retrieved chunks
    print("\n--- RETRIEVED CHUNKS ---")
    for i, res in enumerate(results):
        print(f"\nResult {i+1} (Score: {res['score']:.4f}):")
        print(f"Title: {res['title']}")
        if res.get('ipc_sections'):
            print(f"Relevant IPC: {', '.join(res['ipc_sections'])}")
        print(f"Chunk: {res['chunk'][:200]}...")

    # 2. Generate RAG Answer
    print("\n--- LLM GENERATED ANSWER (RAG) ---")
    answer = qs.generate_answer(query, results)
    print(answer)

if __name__ == "__main__":
    main()
