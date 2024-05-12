import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

openai.api_key = st.secrets.OPENAI_API_KEY
st.title("Chat with the Streamlit docs, powered by LlamaIndex")

reader = SimpleDirectoryReader(input_dir="./docs", recursive=True)
docs = reader.load_data()
