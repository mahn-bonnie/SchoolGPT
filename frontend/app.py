import streamlit as st
import requests
from datetime import datetime, timedelta
import time

# Sidebar with buttons
with st.sidebar:
    st.title('💬OdolGPT🤖')
    
    if st.button('New Chat'):
        st.session_state.messages = []  # Clear messages
        st.session_state.current_date = None  # Reset current date
        st.session_state.selected_chat = None  # Reset selected chat
        st.session_state.chat_summaries = {}  # Reset chat summaries

    if st.button('Today'):
        st.session_state.current_date = datetime.today().strftime('%Y-%m-%d')
    
    if st.button('Yesterday'):
        st.session_state.current_date = (datetime.today() - timedelta(1)).strftime('%Y-%m-%d')
    
    if st.button('Previous Chats'):
        st.session_state.current_date = None  # Show all chats

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_date' not in st.session_state:
    st.session_state.current_date = None
if 'selected_chat' not in st.session_state:
    st.session_state.selected_chat = None
if 'chat_summaries' not in st.session_state:
    st.session_state.chat_summaries = {}

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"""
            <div style="border-radius: 1rem; padding: 10px; margin: 5px; {'background-color: snow; color: black;' if message['role'] == 'assistant' else 'background-color: #; color: ;'}">
                {message["content"]}
            </div>
        """, unsafe_allow_html=True)

if prompt := st.chat_input("Message OdolGPT..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"""
            <div style="border-radius: 1rem; padding: 10px; margin: 5px; background-color: #; color: white;">
                {prompt}
            </div>
        """, unsafe_allow_html=True)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner(text="Odol is thinking..."):
            # Add a sleep to simulate thinking time (e.g., 2 seconds)
            time.sleep(2.5)

            try:
                response = requests.post("http://127.0.0.1:8000/chat", json={"content": prompt})
                if response.status_code == 200:
                    full_response = response.json()["response"]
                else:
                    full_response = "Error: " + response.json().get("detail", "Unknown error")
            except Exception as e:
                full_response = f"Error: {e}"

            message_placeholder.markdown(f"""
                <div style="border-radius: 1rem; padding: 10px; margin: 5px; background-color: snow; color: black;">
                    {full_response}
                </div>
            """, unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Chat history summary
def display_chat_summaries():
    if st.session_state.current_date:
        st.subheader(f"Chats for {st.session_state.current_date}")
    else:
        st.subheader("All Chats")

    # Display summaries
    for date, chats in st.session_state.chat_summaries.items():
        if st.session_state.current_date in [None, date]:
            st.write(f"**{date}**")
            for i, chat_summary in enumerate(chats):
                if st.button(f"Chat {i + 1} - {chat_summary}", key=f"chat_{i}"):
                    st.session_state.messages = chat_summary

if st.session_state.current_date or st.session_state.selected_chat is not None:
    display_chat_summaries()

# Additional CSS for hover effect and textarea growth
st.markdown("""
    <style>
    .stTextInput>div>div>textarea {
        overflow: hidden;
        resize: none;
        min-height: 60px;
        max-height: 150px;
        border-radius: 3rem;
    }
    .stTextInput>div>div {
        display: flex;
        flex-direction: column;
    }
    .stTextInput>div>div>textarea:focus {
        box-shadow: 0 0 0 2px #00A36C;
    }
    .thinking-message {
        background-color: #e0e0e0;
        color: #000;
        animation: fadeOut 2.5s forwards;
    }
    @keyframes fadeOut {
        0% {
            opacity: 1;
        }
        100% {
            opacity: 0;
        }
    }
    </style>
""", unsafe_allow_html=True)
