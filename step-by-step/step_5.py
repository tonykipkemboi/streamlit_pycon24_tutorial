import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, Document, SimpleDirectoryReader, Settings

openai.api_key = st.secrets.openai_api_key
st.title("Chat with the Streamlit docs, powered by LlamaIndex ")

reader = SimpleDirectoryReader(input_dir="./docs", recursive=True)
docs = reader.load_data()

Settings.llm = OpenAI(
    model="gpt-3.5-turbo",
    temperature=0.2,
    system_prompt="""You are an expert on 
    the Streamlit Python library and your 
    job is to answer technical questions. 
    Assume that all questions are related 
    to the Streamlit Python library. Keep 
    your answers technical and based on 
    facts – do not hallucinate features."""
    )

index = VectorStoreIndex.from_documents(docs)

chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

prompt = st.chat_input("Ask a question")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)

    response = chat_engine.chat(prompt)
    with st.chat_message("assistant"):
        st.write(response.response)
