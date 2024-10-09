# import google.generativeai as genai
# genai.configure(api_key=os.getenv('API_KEY'))

# model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content(st.text_input("Enter your prompt:"))
# st.write(response.text)

import os
import streamlit as st
from typing import Generator
from groq import Groq

from dotenv import load_dotenv
import streamlit as st

load_dotenv()
st.set_page_config( layout="wide",
                   page_title="Apple Chatbot")


st.title("🕸️SpiV chatbot")
st.subheader("",divider="orange", anchor=False)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


if prompt := st.chat_input("Enter your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    # Fetch response from Groq API
    try:
        chat_completion = client.chat.completions.create(
            model="gemma-7b-it",
            messages=[
                {
                    "role": m["role"],
                    "content": m["content"]
                }
                for m in st.session_state.messages
            ],
            stream=True
        )

        # Use the generator function with st.write_stream
        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)
    except Exception as e:
        st.error(e, icon="🚨")

    # Append the full response to session_state.messages
    if isinstance(full_response, str):
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
    else:
        # Handle the case where full_response is not a string
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": combined_response})