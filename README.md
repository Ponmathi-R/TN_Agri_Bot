# 🌾 TN Agri-Scheme AI Assistant
### Enterprise RAG-Driven Bilingual Knowledge Discovery Engine

An intelligent, production-ready, conversational AI application that provides transparent, real-time access to official Government of Tamil Nadu agricultural resources, funding patterns, and application criteria. 

By leveraging **Retrieval-Augmented Generation (RAG)**, this platform bridges the gap between complex web data layouts and end-users, delivering contextual answers completely in either **English** or **தமிழ் (Tamil)** through an optimized, live-synced knowledge pipeline.

---

## 🏗️ End-to-End System Architecture

The following flowchart illustrates how raw portal content is fetched, transformed into high-dimensional vector matrices, and dynamically retrieved during an active user chat session:

```text
======================= DATA INGESTION PIPELINE (OFFLINE) =======================

 [Official TN Portal] ──> [Headless Selenium Webdriver] ──> [HTML Table Parser]
                                                                  │
                                                                  ▼
 [FAISS Vector Store] <── [HuggingFace Embeddings] <── [Recursive Text Splitter]
    (Local Index)

======================== USER INTERACTION PIPELINE (ONLINE) =======================

 [User Query (EN/TA)] ──> [Streamlit UI Dashboard] ──> [Dynamic Language Router]
                                                                  │
                                                                  ▼
 [Contextual Answer]  <── [Groq API (Llama 3.1 8B)]  <── [FAISS Vector Retrieval]


🌟 Key Features
Anti-Firewall Table Scraper: Automated headless Selenium browser implementation configured with random user-agents to gracefully bypass server-side scraping blocks and parse deep-nested HTML data tables without data drops.

Context-Aware Bilingual Router: Dynamic UI toggle shifts system prompts on-the-fly, coercing the LLM to output structured responses strictly matching the language of choice.

Stateful Memory Isolation: Automatic flush-mechanisms that isolate chat memory structures when flipping between languages to avoid language cross-contamination.

Sandboxed Asset Carousel: Modern st.iframe component embedding designed to deliver a high-end UI experience while adhering strictly to deprecation guardrails.


🛠️ Tech Stack
Our architecture is built intentionally using enterprise-standard open-source layers selected for speed, security, and data privacy:

Layer,Technology,Purpose
Frontend UI,Streamlit,"Lightweight, reactive Python dashboarding"
Automation Engine,Selenium + BeautifulSoup4,Headless DOM traversal & HTML Table matrix mapping
Orchestration,LangChain / Core,Declarative chain configurations and state routing
Embeddings,HuggingFace (all-MiniLM-L6-v2),Local execution of semantic text vector processing
Vector Database,FAISS (Facebook AI Similarity Search),Specialized ultra-fast local vector retrieval index
Inference LLM,Groq API (llama-3.1-8b-instant),Sub-100ms ultra-low latency response compilation


🚀 Quick Start Guide
1. Environment Setup
Clone the repository and instantiate an isolated Python virtual environment:
python -m venv venv
source venv/Scripts/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

2. Configuration
Create a .env file in the root directory and append your secure API credentials:

Code snippet
GROQ_API_KEY=your_secure_groq_api_token_here

3. Compile the Knowledge Base
Trigger the automated scraping web driver to pull live portal rows and compile the FAISS local mathematical matrix:

Bash
python ingest.py

4. Boot the Assistant
Launch the Streamlit interactive server locally:

Bash
streamlit run app.py

👥 Production Best Practices & Architectural Notes
Deterministic Filtering: LLM temperature is deliberately locked at 0.1 to eliminate model hallucination risks and enforce total alignment with scanned state records.

Database Isolation: FAISS vector records run locally on the server filesystem (./faiss_agri_index), ensuring zero external cloud transmission of raw portal knowledge tables.

 
