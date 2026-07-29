import streamlit as st
import pickle
import time

# 1. Browser Tab Setup (Title aur Icon)
st.set_page_config(
    page_title="Mera Smart AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# 2. Models Load Karein
@st.cache_resource
def load_models():
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    with open('chatbot_model.pkl', 'rb') as f:
        model = pickle.load(f)
    return vectorizer, model

vectorizer, model = load_models()

# 3. Model Response Logic
def get_response(user_input):
    text_vector = vectorizer.transform([user_input])
    prediction = model.predict(text_vector)
    answer = prediction[0]
    return answer

# 4. Typing Effect Function (Bot reply ko animate karne ke liye)
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.04) # Typing ki speed yahan se adjust kar sakte hain

# 5. Sidebar (Options aur Settings)
with st.sidebar:
    st.title("⚙️ Chatbot Options")
    st.write("Aapka personal AI Assistant.")
    st.divider()
    
    # Clear Chat Button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.caption("Developed with ❤️ using Streamlit")

# 6. Main Chat Title
st.title("🤖 Mera Smart AI Chatbot")
st.caption("💬 Mujhse kuch bhi puchiye, main aapki help karunga!")

# Chat history setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani Chat Display karein (Avatars ke sath)
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Apna message yahan type karein..."):
    # User message show karein
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Model response generate karein
    response = get_response(prompt)

    # Bot response typing animation ke sath show karein
    with st.chat_message("assistant", avatar="🤖"):
        full_response = st.write_stream(stream_data(response))
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})