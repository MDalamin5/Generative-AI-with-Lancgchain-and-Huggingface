from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os

# Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACKING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Q&A Chatbot with Ollama"


## Prompt Template ollama run gemma2:2b
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please response to the user queries"),
        ("user", "Question:{question}")
    ]
)

def generate_response(question,engine, temperature, max_tokens):
    llm = Ollama(model=engine)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({"question": question})
    return answer


## Title of the app
st.title("Enhanced Q&A Chatbot with Open-Source Model")
st.sidebar.title("Settings")
# api_key = st.sidebar.text_input("Enter your Open AI API Key: ", type="password")


## Drop down to select various Open AI Models
llm=st.sidebar.selectbox("Select an open AI Model", ["gemma2:2b", "gpt-4-turbo", "gpt-4"])

## Adjust response parameter

temperature=st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.6)
max_tokens=st.sidebar.slider("Max Tokens", min_value=50, max_value=400, value=150)


## Main interface for user input
st.write("Go ahead and ask any questions")
user_input=st.text_input("You: ")

if user_input:
    response = generate_response(user_input,llm, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please provide the query")