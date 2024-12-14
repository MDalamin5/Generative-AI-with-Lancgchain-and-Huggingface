import validators, streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader


## streamlit app

st.set_page_config(page_title="LangChain: Summarize Text from YT or Website", page_icon="🦜️")
st.title("🦜️ LangChain: Summarize Text from YT or Website")
st.subheader("Summarize URL")

## get greq api key and url field to be summarized

with st.sidebar:
    groq_api_key=st.text_input("Groq API KEY", value="", type="password")

url=st.text_input("URL", label_visibility="collapsed")