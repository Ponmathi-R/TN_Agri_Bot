import streamlit as st
from core import get_rag_chain

st.set_page_config(
    page_title="TN Agri-Scheme AI Assistant",
    page_icon="🌾",
    layout="centered"
)

if "language" not in st.session_state:
    st.session_state.language = "English"

# --- SIDEBAR SETUP ---
with st.sidebar:
    st.markdown(
        """
        <div style="background-color: #f0f7f4; border-left: 5px solid #2e7d32; padding: 12px; border-radius: 6px; text-align: center; margin-bottom: 15px;">
            <span style="font-size: 28px;">🏛️</span>
            <h4 style="margin: 5px 0 0 0; color: #1b5e20; font-family: sans-serif;">தமிழ்நாடு அரசு</h4>
            <small style="color: #4e5d4c; font-weight: bold;">Government of Tamil Nadu</small>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown("### **அமைப்பு / Settings**")
    selected_lang = st.radio("தேர்ந்தெடு / Select Language:", ["English", "தமிழ்"])
    
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        if "messages" in st.session_state:
            del st.session_state["messages"]

    st.divider()
    
    if st.session_state.language == "English":
        st.markdown("### 🌾 **Farmer Motivation**")
        st.info('"To a farmer, agriculture is not a business, it is a way of life."\n\n**Let us honor the hands that feed us!**')
    else:
        st.markdown("### 🌾 **விவசாயி ஊக்கம்**")
        st.success('"உழவுக்கும் தொழிலுக்கும் வந்தனை செய்வோம்!"\n\n**நமக்குப் படியளக்கும் கரங்களை போற்றுவோம்!**')

localization = {
    "English": {
        "title": "Government of Tamil Nadu",
        "subtitle": "🌾 Agriculture Scheme AI Assistant",
        "desc": "Welcome! This intelligent assistant provides quick, transparent access to official Tamil Nadu state agricultural resources.",
        "input_placeholder": "Ask about seeds, subsidies, fertilizers, or training...",
        "bot_greet": "Vanakkam! I am your Agriculture Assistant. How can I help you find or understand an official scheme today?",
        "spinner": "Searching official portal records...",
        "error": "An error occurred: "
    },
    "தமிழ்": {
        "title": "தமிழ்நாடு அரசு",
        "subtitle": "🌾 விவசாய திட்டங்கள் AI உதவியாளர்",
        "desc": "வரவேற்கிறோம்! இந்த நுண்ணறிவு உதவியாளர் தமிழ்நாடு அரசின் அதிகாரப்பூர்வ விவசாய திட்டங்கள் மற்றும் மானிய விவரங்களை உங்களுக்கு எளிமையாக விளக்கும்.",
        "input_placeholder": "விதை, மானியம், உரம் அல்லது பயிற்சிகள் பற்றி கேளுங்கள்...",
        "bot_greet": "வணக்கம்! நான் உங்கள் விவசாய உதவியாளர். இன்று எந்த அரசுத் திட்டத்தைப் பற்றி தெரிந்துகொள்ள விரும்புகிறீர்கள்?",
        "spinner": "அதிகாரப்பூர்வ பதிவுகளைத் தேடுகிறது...",
        "error": "பிழை ஏற்பட்டது: "
    }
}

text = localization[st.session_state.language]

# --- AUTOMATIC CAROUSEL ---
images = [
    "https://static.vecteezy.com/system/resources/thumbnails/019/925/387/small_2x/lettuce-plant-on-field-vegetable-and-agriculture-sunset-and-light-free-photo.jpg",
    "https://images.unsplash.com/photo-1620200423727-8127f75d7f53?fm=jpg&q=80&w=1200",
    "https://img.freepik.com/premium-photo/3d-illustration-smart-robotic-futuristic-farmers-working-field-agriculture-technology-farm-automation_564714-292.jpg?w=1200"
]

carousel_html = f"""
<div style="width: 100%; overflow: hidden; border-radius: 12px; margin-bottom: 20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.15);">
    <div style="display: flex; width: 300%; animation: slide 15s infinite ease-in-out;">
        <div style="width: 100%;"><img src="{images[0]}" style="width: 100%; height: 320px; object-fit: cover;"></div>
        <div style="width: 100%;"><img src="{images[1]}" style="width: 100%; height: 320px; object-fit: cover;"></div>
        <div style="width: 100%;"><img src="{images[2]}" style="width: 100%; height: 320px; object-fit: cover;"></div>
    </div>
</div>
<style>
@keyframes slide {{
    0% {{ transform: translateX(0%); }}
    28% {{ transform: translateX(0%); }}
    33% {{ transform: translateX(-33.33%); }}
    61% {{ transform: translateX(-33.33%); }}
    66% {{ transform: translateX(-66.66%); }}
    95% {{ transform: translateX(-66.66%); }}
    100% {{ transform: translateX(0%); }}
}}
</style>
"""
st.iframe(src="data:text/html;charset=utf-8," + carousel_html, height=330)

st.subheader(text["title"])
st.title(text["subtitle"])
st.markdown(text["desc"])
st.divider()

# Instantiate the active language configuration
rag_chain = get_rag_chain(st.session_state.language)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": text["bot_greet"]}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_prompt := st.chat_input(text["input_placeholder"]):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner(text["spinner"]):
            try:
                ai_response = rag_chain.invoke(user_prompt)
                response_placeholder.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                response_placeholder.error(f"{text['error']}{e}")