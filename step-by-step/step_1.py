import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

openai.api_key = st.secrets.openai_api_key
st.title("Chat with the Streamlit docs, powered by LlamaIndex")
