# llm_utils.py

import openai
import streamlit as st


def get_response_stream(api_key, messages, model, temperature=0.2, max_tokens=256):
    try:
        client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

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
        yield f"Error: {str(e)}"
