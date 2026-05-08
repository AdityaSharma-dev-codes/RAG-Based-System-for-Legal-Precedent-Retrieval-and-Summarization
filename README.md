# RAG-Based System for Legal Precedent Retrieval and Summarization

> **Work in Progress:** This project is under active development and some features may be incomplete or unstable.  
> **Academic Project:** This is a major college project and a team effort.

A Retrieval-Augmented Generation (RAG) system for the Indian judiciary, enabling semantic search and LLM-generated summaries of relevant legal precedents from the Indian Supreme Court.

### Features

- **Semantic Search**: Retrieve legal cases based on case context and legal principles.
- **Automated Summarization**: Generate concise summaries for complex legal documents.
- **Document Processing**: Automated text extraction and classification from case PDFs.
- **Indian Judiciary Focus**: Specifically designed to handle the nuances of Indian legal documents (e.g., IPC, CrPC).

### Project Structure

- `DataSet/`: Organized by year (2000-2025), containing Supreme Court case PDFs.
- `extract.py`: Script to extract text from PDFs and classify criminal cases based on keywords.
- `clean.py`: Robust script to clean judgment text, standardize IPC sections, and deduplicate cases.
- `chunk_judgments.py`: Script to divide long judgment texts into manageable chunks for processing.
- `test.py`: Validation script to verify data quality and track missing information.
- `test_chunks.py`: Validation script to ensure chunked data meets word count constraints.
- `LICENSE`: MIT License.
- `criminal_cases.json`: Initial extracted text from the DataSet.
- `Cleaned_criminal_cases.json`: Final cleaned and enriched JSON dataset.
- `Chunked_criminal_cases.json`: Dataset with judgments divided into chunks.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/adityasharma-dev-codes/RAG-Based-System-for-Legal-Precedent-Retrieval-and-Summarization.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt 
   ```

### Usage

1. **Extraction**: To process the dataset and identify criminal cases:
   ```bash
   python extract.py
   ```
   The script traverses the `DataSet/` directory, extracts text from each PDF, and outputs whether it qualifies as a criminal case based on keywords (e.g., "IPC", "State vs").
<br><br>

2. **Cleaning**: To clean and enrich the extracted data:
   ```bash
   python clean.py
   ```
   This script performs:
   - **Judgment Formatting**: Removes boilerplate (headers, dates) and normalizes whitespace/newlines into a single clean paragraph.
   - **IPC Extraction**: Uses advanced regex to re-extract IPC sections from judgment text with 99% accuracy.
   - **Standardization**: Normalizes IPC section strings (e.g., "Section 302 IPC").
   - **Deduplication**: Removes duplicate cases based on title and judgment content.
<br><br>

3. **Chunking**: To divide judgments into smaller segments:
   ```bash
   python chunk_judgments.py
   ```
   This script:
   - **Sentence-based Chunking**: Uses SpaCy's `sentencizer` to group sentences into chunks of up to 300 words.
   - **Handling Long Judgments**: Successfully processes extremely long texts by increasing SpaCy's `max_length` limit.
   - **Word Limit Enforcement**: Forcibly splits sentences that exceed the maximum word count to ensure all chunks are within the 300-word limit.
<br><br>

4. **Validation**: To check the quality of the dataset:
   ```bash
   python test.py
   python test_chunks.py
   ```
   These scripts perform:
   - **Missing Data Check (test.py)**: Counts missing values in `title`, `judgment`, and `ipc_sections` for both original and cleaned datasets.
   - **Word Count Statistics (test.py)**: Calculates the average, minimum, and maximum word counts in the `judgment` section.
   - **Chunk Validation (test_chunks.py)**: Verifies that no chunk in `Chunked_criminal_cases.json` exceeds the 300-word limit and provides chunk-level statistics.
<br><br>

5. **Vectorization**: To generate embeddings and build the search index:
   ```bash
   python vectorize.py
   ```
   This script:
   - **SBERT Embeddings**: Uses the `all-MiniLM-L6-v2` model to convert text chunks into 384-dimensional dense vectors.
   - **FAISS Indexing**: Builds a high-performance vector index using Cosine Similarity (via `IndexFlatIP` and L2 normalization).
   - **Batch Processing**: Optimized to handle 120k+ chunks in minutes.
<br><br>

6. **RAG (Retrieval-Augmented Generation)**: To get answers based on retrieved legal chunks:
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   python query_system.py
   ```
   This system features:
   - **Semantic Retrieval**: Finds relevant case chunks based on legal queries rather than just keywords.
   - **LLM-Generated Answers**: Uses Google Gemini (via `google-generativeai`) to explain retrieved legal contexts and answer queries.
   - **IPC-Aware Results**: Automatically highlights relevant IPC sections associated with the retrieved legal precedents.

### Team Members
- Aditya Sharma (Team Lead)  
- Alvin Mike Jerad  
- Aswin

### Acknowledgements

Dataset (Court Cases PDFs): [SC Judgments (India, 1950–2024)](https://www.kaggle.com/datasets/adarshsingh0903/legal-dataset-sc-judgments-india-19502024)

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
