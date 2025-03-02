# 1_chat.py

import streamlit as st
from llm_utils import get_response_stream

st.title("💬 Chat with LLM")

openrouter_api_key = st.text_input("OpenRouter API Key", type="password")
system_prompt = st.text_area(
    "System Prompt", placeholder="Enter the system prompt here...")

# Define models dictionary
MODELS = {
    "chatgpt-4o-latest": "openai/chatgpt-4o-latest",
    "o3-mini-high": "openai/o3-mini-high",
    "claude-3.7-sonnet": "anthropic/claude-3.7-sonnet",
    "claude-3.7-sonnet:thinking": "anthropic/claude-3.7-sonnet:thinking"
}


def clear_chat_history():
    st.session_state.messages = []


def main():
    if not openrouter_api_key:
        st.info("Please add your OpenRouter API key to continue.", icon="🗝️")
    else:
        # Initialize session state for messages
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Sidebar for model selection
        choice = st.sidebar.selectbox("Select a model", list(MODELS.keys()))
        temperature = st.sidebar.slider(
            'temperature', min_value=0.01, max_value=2.0, value=0.4, step=0.01)
        max_tokens = st.sidebar.slider(
            'max_tokens', min_value=1024, max_value=16384, value=4096, step=128)

        st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

        # Display chat messages from the session state
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Input prompt from user
        if prompt := st.chat_input("Type your message here"):
            # Add system prompt to chat history if provided
            if system_prompt and {"role": "system", "content": system_prompt} not in st.session_state.messages:
                st.session_state.messages.insert(
                    0, {"role": "system", "content": system_prompt})

            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append(
                {"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                response = st.write_stream(get_response_stream(
                    openrouter_api_key, st.session_state.messages, MODELS[choice], temperature=temperature, max_tokens=max_tokens))
            st.session_state.messages.append(
                {"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
