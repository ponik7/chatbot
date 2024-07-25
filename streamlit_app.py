import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")


def get_response_stream(messages, model, temperature=0.2, max_tokens=256):
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            yield content
    except Exception as e:
        return f"Error: {str(e)}"


# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenRouter API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openai_api_key,
    )

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your message here"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append(
            {"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            response = st.write_stream(get_response_stream(
                st.session_state.messages, MODELS[choice], temperature=temperature, max_tokens=max_tokens))
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
