import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
import os
from dotenv import load_dotenv
load_dotenv()
import time

groq_api_key=os.getenv("GROQ_API_KEY")

llm = ChatGroq(groq_api_key=groq_api_key,model_name="qwen-2.5-coder-32b")

prompt = ChatPromptTemplate.from_template(
    """
    Answer the question based on the provided context only.
    Please provide the most accurate respond based on the question
    <context>
    {context}
    <context>
    Question:{input}
    """
)

def create_vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        st.session_state.loader=PyPDFDirectoryLoader('pdf_data')
        st.session_state.docs=st.session_state.loader.load()
        st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        st.session_state.final_documents=st.session_state.text_splitter.split_documents(st.session_state.docs[:50])
        st.session_state.vectors=FAISS.from_documents(st.session_state.final_documents, st.session_state.embedding)
        
user_prompt = st.text_input("Enter your query from the research paper.")

if st.button("Document Embedding"):
    create_vector_embedding()
    st.write("Your Vector db is ready")
    

if user_prompt:
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retriever_chain = create_retrieval_chain(retriever, document_chain)
    response = retriever_chain.invoke({'input': user_prompt})
    # st.write(response['answer'])
    
    def stream_data():
        for word in response['answer'].split(" "):
            yield word + " "
            time.sleep(0.02)

   
    st.write_stream(stream_data)
    
    with st.expander("DOcument similirity Search"):
        for i, doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write("___________________________")
        



