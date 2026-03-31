# ILPM: RAG-Based Legal Precedent Retrieval & Summarization

### IMPORTANT
> **Work in Progress:** This project is under active development and some features may be incomplete or unstable.  
> **Academic Project:** This is a major college project and a team effort.

**Team Members:**  
- Aditya Sharma (Team Lead)  
- Alvin Mike Jerad  
- Aswin   
 

A Retrieval-Augmented Generation (RAG) system for the Indian judiciary, enabling semantic search and LLM-generated summaries of relevant legal precedents from the Indian Supreme Court.

### Features

- **Semantic Search**: Retrieve legal cases based on case context and legal principles.
- **Automated Summarization**: Generate concise summaries for complex legal documents.
- **Document Processing**: Automated text extraction and classification from case PDFs.
- **Indian Judiciary Focus**: Specifically designed to handle the nuances of Indian legal documents (e.g., IPC, CrPC).

### Project Structure

- `DataSet/`: Organized by year (2000-2025), containing Supreme Court case PDFs.
- `extract.py`: Script to extract text from PDFs and classify criminal cases based on keywords.
- `LICENSE`: MIT License.

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

To process the dataset and identify criminal cases:
```bash
python extract.py
```

The script will traverse the `DataSet/` directory, extract text from each PDF, and output whether it qualifies as a criminal case based on predefined keywords (e.g., "IPC", "State vs").

**Team Members:**  
- Aditya Sharma (Team Lead)  
- Alvin Mike Jerad  
- Aswin

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
