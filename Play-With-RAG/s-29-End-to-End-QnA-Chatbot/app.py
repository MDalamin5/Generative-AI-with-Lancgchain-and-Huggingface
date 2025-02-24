from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "QnA Chatbot with Groq"

## Prompt template
prompt=ChatPromptTemplate.from_messages(
    [
        ('system',"You are a Helpful ai assistant and response user question"),
        ("user", "Question:{question}")
    ]
)

def generate_response(question, api_key, llm, temperature, max_token):
    
    os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
    # llm = ChatGroq(groq_api_key = api_key, model_name = llm)
    llm = ChatGroq(model_name=llm)
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer


## app
st.title("title of my chat bot")

## sidebar
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your Gorq api key", type='password')

## create dropdown to select various things
llm = st.sidebar.selectbox("Select you Model", ['qwen-2.5-32b', 'deepseek-r1-distill-qwen-32b', 'gemma2-9b-it'])
## adjust temperature value
temperature=st.sidebar.slider("Temperature",min_value=0.0, max_value=1.0, value=0.8)
max_token=st.sidebar.slider("Max_token",min_value=60, max_value=350, value=130)

## define the main interface
st.write("Go ahead and ask any questions")
# user_input = st.chat_input("You: ")
user_input = st.text_input("You: ")

if user_input:
    response = generate_response(user_input, api_key, llm, temperature, max_token)
    st.write(response)
else:
    st.write("Please provide the query")