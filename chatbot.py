import google.generativeai as genai
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
genai.configure(api_key=os.getenv('API_KEY'))

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(st.text_input("Enter your prompt:"))
st.write(response.text)