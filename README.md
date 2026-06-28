# TN_Agri_Bot
AI-powered bilingual RAG assistant for Tamil Nadu agriculture schemes. Uses Nomic embeddings, local FAISS index, and Llama 3 on Ollama for private, fact-checked retrieval. Farmer queries in English or Tamil trigger dynamic search logs in the cute, accessible Streamlit UI.


# 🌾 TN Agri Advisor RAG System

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/8/81/Tamil_Nadu_Emblem.png" width="120" alt="TN Emblem">
  <br>
  <strong>A Bilingual GenAI + RAG assistant for exploring Tamil Nadu Government Agriculture Schemes.</strong>
</p>

## 🎯 Project Goal
The **TN Agri Advisor RAG System** is a production-grade, offline-first application built to bridge the gap between complex government policies and the immediate needs of farmers in Tamil Nadu. The goal is to provide a beautiful, cute, private AI interface that accepts questions in English and தமிழ், searches the official government scheme list (tn.gov.in), transparently displays its vector thought process, and generates verified answers with local precision.

## ⚙️ System Flow & Architecture
This project uses a Retrieval-Augmented Generation (RAG) architecture running entirely on your local machine using Ollama and local vector stores, ensuring maximum data privacy for agricultural stakeholders.

Below is the visualized step-by-step pipeline from data ingestion to user interaction, complete with miniature icons detailing each structural component:

![System Data Pipeline](creative_agri_infographic.png)

### Architecture Highlights
* **Step 1–4 (Offline Ingestion):** Official HTML data is scraped, parsed, split into exact 1200-character fragments, vectorized using local **Nomic Embeddings**, and saved locally in a **FAISS Index**.
* **Step 5–8 (Online Inference):** User queries (in either language) trigger a local similarity search. The first few matching document chunks are transparently printed to the user's thought log panel before being fed into a local **Llama 3** engine to stream the final, private response.

## 📂 Project Repository Tree
```text
tn-agri-chatbot/
│
├── faiss_index/              # Local folder containing the vector database files
│   ├── index.faiss           # Structural vector tensors
│   └── index.pkl             # Serialized document metadata pickle
│
├── .env                      # Local parameters and token configurations
├── creative_agri_infographic.png  # The system flowchart visual map
├── requirements.txt          # Active library compilation list
└── tn_rag_app.py            # Primary main Streamlit application source file
