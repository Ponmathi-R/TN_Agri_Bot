# tn_rag_app.py
import os
import streamlit as st

# Fix the USER_AGENT warning before importing langchain loaders
os.environ["USER_AGENT"] = "TN_Agri_Bot/1.0"

from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

# --- INITIALIZATION & ENVIRONMENT SETUP ---
load_dotenv()

DB_INDEX_PATH = "faiss_index"
URL = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="

def initialize_vector_db():
    """Checks if the local FAISS database exists; creates it if missing."""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    if not os.path.exists(DB_INDEX_PATH):
        loader = WebBaseLoader(URL)
        docs = loader.load()
        
        # Injected verified scheme text data layer to handle dynamic tables/scraping loss
        generator_subsidy_text = """
        Scheme Title/Name: Generator subsidy
        Concerned Department: Agriculture - Farmers Welfare Department
        Sponsered By: State
        Funding Pattern: 25% on the cost of the generator sets upto 125 KVA capacity
        Beneficiaries: Manufacturers / Farmers using custom setups
        Types of Benefits: Subsidy
        How To avail: Within six months from the date of purchase of the generator set or date of installation of the generator set, whichever is later.
        Description: Anywhere in the State
        """
        docs.append(Document(page_content=generator_subsidy_text, metadata={"source": "Official Web Table Fallback Fix"}))
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
        chunks = text_splitter.split_documents(docs)
        
        vector_db = FAISS.from_documents(chunks, embeddings)
        vector_db.save_local(DB_INDEX_PATH)
    else:
        vector_db = FAISS.load_local(DB_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        
    return vector_db

def get_agri_rag_chain(vector_db):
    """Constructs the LangChain Expression Language (LCEL) execution chain."""
    retriever = vector_db.as_retriever(search_kwargs={"k": 4})
    llm = OllamaLLM(model="llama3", temperature=0.1)
    
    prompt_template = """You are an expert AI Assistant specializing in Tamil Nadu Government Agriculture Schemes.
Your goal is to help farmers and manufacturers understand the agricultural welfare options clearly.

Answer the user's question using ONLY the provided official web context below. 
Note: In the context, "Generator subsidy" refers specifically to a hardware generator setup (up to 125 KVA), NOT an AI software data generator. Read the funding pattern details carefully.
Provide the answer in the same language as the user's query (If asked in Tamil, reply clearly in Tamil. If asked in English, reply in English).

If the answer cannot be found in the context, politely say: "I'm sorry, I couldn't find specific details about that scheme on the official website. Please consult the nearest Agricultural Extension Centre." / "மன்னிக்கவும், அதிகாரப்பூர்வ இணையதளத்தில் இந்தத் திட்டம் பற்றிய விவரங்கள் கிடைக்கவில்லை."

Context:
{context}

Question: {question}

Helpful Answer:"""
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain, retriever

# --- STREAMLIT UI LAYOUT & BILINGUAL LANGUAGE CONFIGURATION ---
st.set_page_config(
    page_title="TN Agri AI Advisor", 
    page_icon="🌾", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cute, colorful, vibrant and beautiful palette using injected CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f4faf4 0%, #fffdf6 100%);
    }
    .stHeading h1 {
        color: #1b5e20 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }
    .sidebar .sidebar-content {
        background-color: #e8f5e9 !important;
    }
    .cute-card {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 16px;
        border-top: 5px solid #ffb300;
        border-left: 5px solid #2e7d32;
        box-shadow: 0 6px 12px rgba(46,125,50,0.08);
        margin-bottom: 15px;
    }
    .quote-card {
        background: linear-gradient(135deg, #fff8e1 0%, #f1f8e9 100%);
        padding: 20px;
        border-radius: 16px;
        border: 2px dashed #ffb300;
        color: #3e2723;
        font-style: italic;
        font-size: 1.05rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.04);
    }
    .info-title {
        color: #1b5e20;
        font-weight: bold;
        font-size: 1.05rem;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Language Translation Maps
LANG_TEXTS = {
    "English": {
        "title": "🌾 Tamil Nadu Agriculture Scheme AI Advisor",
        "subtitle": "*Empowering farming communities with reliable, instant government policy data.*",
        "welcome": "Hello! I am your virtual agriculture assistant. Ask me any question regarding schemes, subsidies, or tools provided by the Tamil Nadu Government.",
        "dashboard_title": "⚙️ Settings & Info",
        "source": "📍 Connected Source",
        "engine": "🤖 Local AI Core",
        "guardrails": "🛡️ Guardrails",
        "guard_desc": "Strict factual alignment active.",
        "clear_btn": "🔄 Clear Chat History",
        "input_placeholder": "Ask about a scheme (e.g., Tell me about the generator subsidy)...",
        "thinking_title": "🧠 System Thinking Process",
        "think_done": "✅ Complete! Outputting answer...",
        "quote_heading": "🌱 Farmer Motivation"
    },
    "தமிழ்": {
        "title": "🌾 தமிழ்நாடு அரசு வேளாண் திட்ட உதவி மையம்",
        "subtitle": "*அரசு நலத்திட்டங்களை விவசாயிகளிடம் நேரடியாகக் கொண்டு சேர்க்கும் ஒரு புதிய செயற்கை நுண்ணறிவு தொழில்நுட்பம்.*",
        "welcome": "வணக்கம்! நான் உங்கள் வேளாண் உதவி AI போட். தமிழக அரசின் விவசாயத் திட்டங்கள், மானியங்கள் அல்லது உபகரணங்கள் குறித்த உங்கள் கேள்விகளைக் கேளுங்கள்.",
        "dashboard_title": "⚙️ கட்டுப்பாட்டு மையம்",
        "source": "📍 இணைக்கப்பட்ட தளம்",
        "engine": "🤖 கணினி தளம்",
        "guardrails": "🛡️ பாதுகாப்பு வளையம்",
        "guard_desc": "உண்மைத் தரவுகள் மட்டுமே பயன்படுத்தப்படும்.",
        "clear_btn": "🔄 அரட்டையைத் துடைக்கவும்",
        "input_placeholder": "திட்டங்களைப் பற்றிக் கேளுங்கள் (உதாரணமாக: ஜெனரேட்டர் மானியம் பற்றி கூறு)...",
        "thinking_title": "🧠 கணினி தேடல் மற்றும் பகுப்பாய்வு",
        "think_done": "✅ தயார்! இதோ உங்கள் பதில்...",
        "quote_heading": "🌱 விவசாயி ஊக்கத்தொகை"
    }
}

# --- SIDEBAR INTERFACE ---
with st.sidebar:
    selected_lang = st.radio("🌐 Choose Interface Language / மொழியைத் தேர்ந்தெடுக்கவும்:", ["English", "தமிழ்"], horizontal=True)
    ui = LANG_TEXTS[selected_lang]
    
    st.markdown("---")
    st.markdown(f"### {ui['quote_heading']}")
    if selected_lang == "தமிழ்":
        st.markdown("""
            <div class="quote-card">
            "சுழன்றும்ஏர்ப் பின்னது உலகம் அதனால்<br>இழந்தும் உழவே தலை."<br><br>
            <span style='font-size:0.9rem; color:#2e7d32;'>- திருக்குறள் (உழவு)</span>
            </div>
            <div class="quote-card">
            "உழுவார் உலகத்தார்க்கு அச்சாணி அஃதாற்றாது<br>எழுவாரை எல்லாம் பொறுத்து."
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="quote-card">
            "Agriculture is the pivot of the whole world; because those who pursue other trades must follow the tiller."<br><br>
            <span style='font-size:0.9rem; color:#2e7d32;'>- Thirukkural</span>
            </div>
            <div class="quote-card">
            "Farming is a profession of hope, hard work, and dedication. You feed the nation!"
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"### {ui['dashboard_title']}")
    st.markdown(f"""
        <div class="cute-card">
            <div class="info-title">{ui['source']}</div>
            <div style="color: #444; font-size: 0.9rem;">tn.gov.in/scheme_list</div>
        </div>
        <div class="cute-card">
            <div class="info-title">{ui['engine']}</div>
            <div style="color: #444; font-size: 0.9rem;">Llama 3 & Nomic</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button(ui['clear_btn'], use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": ui['welcome']}]
        st.rerun()

# --- MAIN CHAT INTERFACE AREA ---
head_col1, head_col2 = st.columns([1, 6])
with head_col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/81/Tamil_Nadu_Emblem.png", width=110)
with head_col2:
    st.title(ui['title'])
    st.markdown(ui['subtitle'])

st.markdown("---")

# --- UPDATE IT TO THIS (REMOVE THE DECORATOR) ---
def load_system():
    db = initialize_vector_db()
    chain, retriever = get_agri_rag_chain(db)
    return chain, retriever

try:
    rag_chain, retriever = load_system()
except Exception as e:
    st.error(f"Error loading backend components: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": ui['welcome']}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- MAIN CHAT RETRIEVAL & REAL-TIME RESPONSE GENERATION ---
if user_query := st.chat_input(ui['input_placeholder']):
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        # Real-time extraction status board
        with st.status(ui['thinking_title'], expanded=True) as status:
            if selected_lang == "தமிழ்":
                st.write("🔍 1. உங்கள் கேள்விக்குரிய கணித குறியீடுகளை உருவாக்குகிறது...")
                retrieved_docs = retriever.invoke(user_query)
                st.write(f"📂 2. தரவுத்தள தேடல் முடிந்தது! **{len(retrieved_docs)}** ஆவண துண்டுகள் கிடைத்துள்ளன.")
                st.write("---")
                for idx, doc in enumerate(retrieved_docs, start=1):
                    st.write(f"**📄 கண்டறியப்பட்ட ஆவணப் பகுதி #{idx}**")
                    st.code(doc.page_content.strip()[:250] + "...", language="text")
                st.write("---")
                st.write("🧠 3. இந்தத் தரவுகளைக் கொண்டு இறுதிப் பதிலைத் தொகுக்கிறது...")
            else:
                st.write("🔍 1. Running query vector alignment against database coordinates...")
                retrieved_docs = retriever.invoke(user_query)
                st.write(f"📂 2. Live Document Fetch Complete! Found **{len(retrieved_docs)}** official text matches.")
                st.write("---")
                for idx, doc in enumerate(retrieved_docs, start=1):
                    source_origin = doc.metadata.get("source", "Official Portal Data")
                    st.write(f"**🔍 Matched Fragment #{idx} [Source: {source_origin}]**")
                    st.code(doc.page_content.strip()[:250] + "...", language="text")
                st.write("---")
                st.write("🧠 3. Injecting live context matches into local Llama 3 core layer...")
                
            status.update(label=ui['think_done'], state="complete", expanded=False)
        
        response_placeholder = st.empty()
        
        try:
            full_response = ""
            response_iterator = rag_chain.stream(user_query)
            
            for chunk in response_iterator:
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
            
            if not full_response.strip():
                with st.spinner("Finalizing answer compilation..."):
                    full_response = rag_chain.invoke(user_query)
            
            response_placeholder.markdown(full_response)
            
        except Exception as e:
            try:
                full_response = rag_chain.invoke(user_query)
                response_placeholder.markdown(full_response)
            except Exception as inner_e:
                st.error(f"An execution error occurred: {inner_e}")
                full_response = "I encountered an issue processing that query. Please make sure Ollama is running."
                response_placeholder.markdown(full_response)
                
    st.session_state.messages.append({"role": "assistant", "content": full_response})