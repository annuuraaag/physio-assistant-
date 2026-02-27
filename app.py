import streamlit as st
from rag_graph import run_assistant

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="PhysioAI Assistant",
    page_icon="🩺",
    layout="wide"
)

# ---------- TITLE ----------
st.title("🩺 AI Physiotherapy Assistant")
st.markdown(
    "Get safe, evidence-based rehabilitation guidance powered by AI."
)

# ---------- SESSION MEMORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("⚙️ Assistant Info")

    st.markdown("""
    **Features:**
    ✔ RAG from physiotherapy guidelines  
    ✔ Intent understanding  
    ✔ Safety guardrails  
    ✔ Rehab advice format  
    ✔ Multi-turn memory  

    ⚠️ This tool does NOT provide medical diagnosis.
    """)

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------- CHAT DISPLAY ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- USER INPUT ----------
user_input = st.chat_input("Describe your pain or injury...")

if user_input:

    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # ---------- CALL BACKEND ----------
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your condition..."):

            response = run_assistant(user_input)

            st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )