import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

import os
from dotenv import load_dotenv
load_dotenv()
import time


os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")
embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

## set up streamlit app
st.title("Conversational Rag With Pdf uploads and chat History")
st.write("Upload your pdf")

api_key = st.text_input("Enter your Groq api Key!", type='password')

if api_key:
    llm = ChatGroq(groq_api_key=api_key,model_name="qwen-2.5-coder-32b")
    
    session_id=st.text_input("Session ID",value="default_session")