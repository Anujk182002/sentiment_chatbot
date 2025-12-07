import streamlit as st
from analyzer import SentimentEngine
from llm_service import LLMEngine

# Page Config
st.set_page_config(page_title="Smart Sentiment Chatbot", page_icon="🤖")
st.title("🤖 Smart Chatbot with Groq & VADER")

# --- 1. Setup API Key ---
# Best practice: Use st.secrets, but for this assignment, a sidebar input is easy
api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

if not api_key:
    st.info("Please enter your Groq API Key in the sidebar to start.")
    st.stop()

# --- 2. Initialize State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "sentiment_engine" not in st.session_state:
    st.session_state.sentiment_engine = SentimentEngine()
if "llm_engine" not in st.session_state:
    st.session_state.llm_engine = LLMEngine(api_key)

# --- 3. Sidebar: Tier 1 Analytics ---
st.sidebar.header("Analytics")
if st.session_state.messages:
    summary = st.session_state.sentiment_engine.analyze_conversation(st.session_state.messages)
    st.sidebar.info(f"**Conversation Mood:**\n{summary}")
    
    if st.sidebar.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# --- 4. Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        # Tier 2: Display sentiment tag for User
        if msg["role"] == "User" and "sentiment_label" in msg:
            label = msg["sentiment_label"]
            score = msg["score"]
            color = "green" if label == "Positive" else ("red" if label == "Negative" else "gray")
            st.caption(f":{color}[Sentiment: {label} ({score:.2f})]")

# --- 5. Main Chat Loop ---
if prompt := st.chat_input("Type your message..."):
    # A. Display User Message
    with st.chat_message("User"):
        st.write(prompt)

    # B. Analyze Sentiment (VADER) - Tier 2 Requirement
    # We analyze BEFORE sending to LLM so we can track user mood
    scores = st.session_state.sentiment_engine.analyze_text(prompt)
    label = st.session_state.sentiment_engine.get_sentiment_label(scores['compound'])
    
    # Show sentiment tag immediately
    color = "green" if label == "Positive" else ("red" if label == "Negative" else "gray")
    with st.chat_message("User"):
        st.caption(f":{color}[Sentiment: {label} ({scores['compound']:.2f})]")

    # C. Store User Message
    st.session_state.messages.append({
        "role": "User",
        "content": prompt,
        "score": scores['compound'],
        "sentiment_label": label
    })

    # D. Get AI Response (Groq)
    # We pass the full history so the LLM has context (Tier 1 Requirement)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text = st.session_state.llm_engine.get_response(st.session_state.messages)
            st.write(response_text)

    # E. Store AI Response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "score": 0 
    })

    # F. Update Analytics
    st.rerun()