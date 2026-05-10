import json
import faiss
from sentence_transformers import SentenceTransformer

def create_test_index():
    print("Creating test data...")
    test_data = [
        {
            "title": "State vs. Sample 1",
            "ipc_sections": ["Section 302 IPC"],
            "chunk": "The punishment for murder under Section 302 IPC is death or imprisonment for life, and shall also be liable to fine. Culpable homicide becomes murder if the act by which the death is caused is done with the intention of causing death."
        },
        {
            "title": "State vs. Sample 2",
            "ipc_sections": ["Section 498A IPC", "Section 438 CrPC"],
            "chunk": "In cases of dowry harassment, the courts have laid down precedents that anticipatory bail under Section 438 CrPC can be granted if the allegations are vague and omnibus. There is no absolute bar on granting anticipatory bail in 498A cases."
        },
        {
            "title": "State vs. Sample 3",
            "ipc_sections": ["Section 120B IPC"],
            "chunk": "The essentials of criminal conspiracy under Section 120B IPC include an agreement between two or more persons to do an illegal act, or an act which is not illegal by illegal means. The very agreement is an offense."
        },
        {
            "title": "State vs. Sample 4",
            "ipc_sections": ["Section 299 IPC", "Section 300 IPC"],
            "chunk": "Culpable homicide not amounting to murder occurs when an act is done with the knowledge that it is likely to cause death, but without any intention to cause death or such bodily injury as is likely to cause death. This distinguishes Section 299 from Section 300."
        }
    ]

    with open("test_subset.json", "w", encoding="utf-8") as f:
        json.dump(test_data, f, indent=4)

    print("Loading SBERT model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    chunks = [item["chunk"] for item in test_data]
    print("Generating embeddings...")
    embeddings = model.encode(chunks, convert_to_numpy=True).astype('float32')
    
    faiss.normalize_L2(embeddings)
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    
    faiss.write_index(index, "test_index.faiss")
    print("Successfully created test_index.faiss and test_subset.json!")

if __name__ == "__main__":
    create_test_index()
