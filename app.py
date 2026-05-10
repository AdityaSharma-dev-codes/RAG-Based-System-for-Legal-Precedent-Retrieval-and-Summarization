import streamlit as st
import os
import time
from query_system import LegalQuerySystem

# --- Page Configuration ---
st.set_page_config(
    page_title="Legal Precedent RAG",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Styling ---
def local_css():
    st.markdown("""
    <style>
    /* Main Background & Text Color */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1c24;
        border-right: 1px solid #2d303a;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #357abd;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Text Area */
    .stTextArea textarea {
        background-color: #262730;
        color: white;
        border: 1px solid #4a90e2;
        border-radius: 8px;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #262730;
        border-radius: 8px;
        color: #e0e0e0;
    }
    
    /* Metrics/Cards */
    div[data-testid="metric-container"] {
        background-color: #262730;
        border: 1px solid #333;
        padding: 5% 5% 5% 10%;
        border-radius: 10px;
        color: #fff;
    }
    
    /* Summary Box */
    .summary-box {
        background-color: #1e222d;
        padding: 20px;
        border-left: 5px solid #4a90e2;
        border-radius: 5px;
        margin-bottom: 20px;
        color: #e0e0e0;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #888;
        font-size: 0.9rem;
        border-top: 1px solid #333;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initialization ---
@st.cache_resource(show_spinner=False)
def load_system():
    index_path = "vector_index.faiss"
    metadata_path = "Chunked_criminal_cases.json"
    
    if not os.path.exists(index_path):
        if os.path.exists("test_index.faiss"):
            index_path = "test_index.faiss"
            metadata_path = "test_subset.json"
        else:
            return None, "Error: FAISS index not found. Please run vectorize.py first to build the index."
            
    try:
        qs = LegalQuerySystem(index_path=index_path, metadata_path=metadata_path)
        return qs, None
    except Exception as e:
        return None, f"Error initializing system: {str(e)}"

# --- UI Components ---

def render_sidebar():
    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>⚖️</h1>", unsafe_allow_html=True)
        st.title("About the Project")
        
        st.markdown("### 📋 Overview")
        st.info(
            "This RAG-based system helps legal professionals quickly retrieve relevant precedents "
            "and generates concise AI-powered summaries, transforming traditional keyword search "
            "into semantic legal discovery."
        )
        
        st.markdown("### 🛠️ Tech Stack")
        st.markdown("""
        - **Frontend**: Streamlit
        - **Retrieval**: FAISS
        - **Embeddings**: SentenceTransformers
        - **LLM**: Google Gemini
        - **Orchestration**: LangChain & Custom Pipeline
        """)
        
        st.markdown("### 👥 Team")
        st.markdown("""
        - **Aditya Sharma**
        - **Alvin Mike Jerad**
        - **Aswin**
        """)

def main():
    local_css()
    
    # Header Section
    st.markdown("<h1 style='text-align: center;'>⚖️ Legal Precedent Retrieval System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; font-size: 1.2rem;'>RAG-Based System for Semantic Search and AI Summarization</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    render_sidebar()
    
    # Load Backend
    with st.spinner("Initializing AI Models and Loading Vector Database..."):
        qs, error_msg = load_system()
        
    if error_msg:
        st.error(error_msg)
        st.warning("Make sure you have run the backend scripts (`extract.py`, `clean.py`, `chunk_judgments.py`, `vectorize.py`) to generate the vector index.")
        return
        
    # Query Section
    st.markdown("### 🔍 Enter Legal Query")
    
    # Example queries
    example_queries = [
        "What is the punishment for murder under IPC 302?",
        "Are there any precedents for anticipatory bail in dowry cases?",
        "What constitutes culpable homicide not amounting to murder?",
        "Explain the essentials of criminal conspiracy."
    ]
    
    # Use session state to handle example button clicks
    if 'query_text' not in st.session_state:
        st.session_state.query_text = ""
        
    # Example query buttons horizontally
    cols = st.columns(len(example_queries))
    for i, ex in enumerate(example_queries):
        if cols[i].button(f"Example {i+1}", help=ex):
            st.session_state.query_text = ex
            
    query = st.text_area(
        "Describe your case or ask a legal question:", 
        value=st.session_state.query_text,
        height=120,
        placeholder="E.g., What are the conditions for granting bail under Section 438 of CrPC?"
    )
    
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        search_clicked = st.button("🚀 Analyze & Retrieve", use_container_width=True)
    with col2:
        k_results = st.number_input("Results Count", min_value=1, max_value=10, value=5, label_visibility="collapsed")
    
    # Process Query
    if search_clicked and query:
        st.session_state.last_query = query
        st.markdown("---")
        st.markdown("### 🤖 Analysis & Results")
        
        # Retrieval Phase
        start_time = time.time()
        with st.spinner("Retrieving relevant precedents from vector database..."):
            results = qs.search(query, k=k_results, threshold=0.3)
            st.session_state.results = results
        retrieval_time = time.time() - start_time
            
        if not results:
            st.warning("No highly relevant legal precedents found for this query. Try rephrasing.")
        else:
            # Generate AI Answer Phase
            with st.spinner("Generating concise legal summary using LLM..."):
                answer = qs.generate_answer(query, results)
                st.session_state.answer = answer
                
            # Display Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Precedents Found", len(results))
            m2.metric("Retrieval Time", f"{retrieval_time:.2f}s")
            m3.metric("Top Relevance", f"{(results[0]['score']*100):.1f}%" if results else "N/A")
            
    # Always display results if they exist in session state
    if 'results' in st.session_state and st.session_state.results:
        results = st.session_state.results
        answer = st.session_state.get('answer', "No summary generated.")
        
        # Display AI Summary
        st.markdown("#### 📝 AI-Generated Summary")
        st.markdown(f"<div class='summary-box'>{answer}</div>", unsafe_allow_html=True)
        
        # Display Retrieved Cases
        st.markdown("#### 📚 Retrieved Legal Precedents")
        
        for i, res in enumerate(results):
            score_pct = res['score'] * 100
            
            # Expandable card for each judgment
            with st.expander(f"📄 {res.get('title', 'Unknown Case')} (Relevance: {score_pct:.1f}%)"):
                st.markdown("**Key Details:**")
                details_cols = st.columns(2)
                with details_cols[0]:
                    if 'ipc_sections' in res and res['ipc_sections']:
                        st.write(f"**IPC Sections:** {', '.join(res['ipc_sections'])}")
                
                st.markdown("**Relevant Judgment Snippet:**")
                st.info(res.get('chunk', 'No snippet available.'))
                
                st.caption(f"Cosine Similarity Score: {res.get('score', 0):.4f}")

    # Footer
    st.markdown(
        """
        <div class="footer">
            <p>Built for Final Year Project | RAG Legal System</p>
            <p style="font-size: 0.8rem;">Disclaimer: AI-generated responses are for reference and educational purposes only. Do not use as professional legal advice.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
