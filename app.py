import streamlit as st  
st.set_page_config(page_title="AI Chatbot", layout="centered")

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from groq import Groq

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GROK_LLM_API_KEY")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH")

if not API_KEY:
    st.error("Groq LLM API Key is missing! Please set GROQ_LLM_API_KEY in your .env file.")
    st.stop()

# Initialize Groq LLM
llm = Groq(api_key=API_KEY)

# Initialize FAISS vector store
if VECTOR_DB_PATH and os.path.exists(VECTOR_DB_PATH):
    vector_store = FAISS.load_local(VECTOR_DB_PATH, HuggingFaceEmbeddings(), allow_dangerous_deserialization=True)
else:
    st.write("⚠️ FAISS index not found! Creating a new index...")
    vector_store = FAISS.from_texts(["sample text"], HuggingFaceEmbeddings())
    if VECTOR_DB_PATH:
        vector_store.save_local(VECTOR_DB_PATH)

# Streamlit UI
st.title("🤖 AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Retrieve relevant context from FAISS vector store
    docs = vector_store.similarity_search(user_input, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    # Generate response from Groq LLM
    prompt = f"Context: {context}\nUser: {user_input}\nAI:"
    
    response = llm.chat.completions.create(
        model="mixtral-8x7b-32768",  # Ensure the correct model name
        messages=[{"role": "user", "content": prompt}]
    )

    bot_reply = response.choices[0].message.content  # Extracting the chatbot's response

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
