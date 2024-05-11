import streamlit as st
import openai
import llama_index

openai.api_key = st.secrets.openai_api_key
st.title("Chat with the Streamlit docs, powered by LlamaIndex")
