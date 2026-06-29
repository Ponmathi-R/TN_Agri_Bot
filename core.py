import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

load_dotenv()

def get_rag_chain(lang="English"):
    """
    Builds the RAG processing chain engine tailored cleanly to the user language choice.
    """
    DB_PATH = "faiss_agri_index"
    
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"[!] Vector Database index not found at {DB_PATH}. Run ingest.py first!")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
    
    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3} 
    )

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.1
    )

    if lang == "தமிழ்":
        system_prompt = (
            "நீங்கள் தமிழ்நாடு அரசின் விவசாயத் துறை திட்ட நிபுணர் AI உதவியாளர்.\n"
            "வழங்கப்பட்ட தகவல்களின் (Context) அடிப்படையில் மட்டுமே விரிவாக பதிலளிக்க வேண்டும்.\n\n"
            "அதிகாரப்பூர்வ பதிவுகள்:\n"
            "{context}\n\n"
            "பதிவின் வடிவமைப்பு கட்டமைப்பு (கட்டாயமாக இந்த 4 பிரிவுகளை மட்டும் பயன்படுத்தவும்):\n"
            "  1. திட்டத்தின் பெயர் (Scheme Name)\n"
            "  2. நிதி உதவி/மானிய விவரம் (Funding Pattern)\n"
            "  3. விண்ணப்பிக்கும் முறை (How To Avail)\n"
            "  4. திட்டத்தின் விளக்கம் (Description)\n\n"
            "முக்கிய விதி: உங்களது முழு பதிலையும் தெளிவான, பிழையற்ற தமிழ் வாக்கியங்களில் மட்டுமே வழங்க வேண்டும். வார்த்தைகளை மீண்டும் மீண்டும் எழுத வேண்டாம்."
        )
    else:
        system_prompt = (
            "You are an expert AI Assistant specializing in Tamil Nadu Government Agriculture Schemes.\n"
            "Your mission is to help farmers understand schemes with absolute clarity based strictly on the context.\n\n"
            "Context provided from the official records:\n"
            "{context}\n\n"
            "Instructions:\n"
            "- Base your answer strictly on the provided context. Do not make things up.\n"
            "- Provide your response completely in clean English prose.\n"
            "- Format your response into these 4 explicit sections:\n"
            "  1. Scheme Name\n"
            "  2. Funding Pattern\n"
            "  3. How To Avail\n"
            "  4. Description\n"
            "- If the scheme details cannot be found in the context, politely say: "
            "'I am sorry, but I couldn't find specific details about that scheme on the official portal content right now.'"
        )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {
            "context": retriever | format_docs, 
            "question": RunnablePassthrough()
        }
        | prompt 
        | llm 
        | StrOutputParser()
    )
    
    return rag_chain