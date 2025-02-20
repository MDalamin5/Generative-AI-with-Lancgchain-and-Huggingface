import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

from langchain_community.llms import ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

## To setup the LangGraph
import os
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful math tutor and provide the answer of the question step by step. Do not give complete answer at a time. Give one step answer and ask to student like do you understand or do you need more clarification? and next student will give a response based in the student response you will provide next step."),
        ("user","Question:{question}")
    ]
)

## streamlit framework
st.title("A simple math tutor")
input_text = st.text_input("What is your question in your mind!")

## groq model
llm = ChatGroq(model_name="qwen-2.5-32b")
## call ollama model
# llm = ollama(model='gemma:2b')
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

if input_text:
    response = chain.invoke(
        {"question": input_text}
    )
    st.write(response)