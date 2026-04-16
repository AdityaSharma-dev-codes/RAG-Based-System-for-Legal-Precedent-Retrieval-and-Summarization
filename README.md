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
- `test.py`: Validation script to verify data quality and track missing information.
- `LICENSE`: MIT License.
- `criminal_cases.json`: Initial extracted text from the DataSet.
- `Cleaned_criminal_cases.json`: Final cleaned and enriched JSON dataset.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/adityasharma-sc/ILPM.git
   cd ILPM
   ```

2. Install dependencies:
   ```bash
   pip install pymupdf
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

3. **Validation**: To check the quality of the dataset:
   ```bash
   python test.py
   ```

### Team Members
- Aditya Sharma (Team Lead)  
- Alvin Mike Jerad  
- Aswin

### Acknowledgements

Dataset (Court Cases PDFs): [SC Judgments (India, 1950–2024)](https://www.kaggle.com/datasets/adarshsingh0903/legal-dataset-sc-judgments-india-19502024)

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
