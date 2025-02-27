import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, load_prompt

groq_api_key=os.getenv("GROQ_API_KEY")

model=ChatGroq(groq_api_key=groq_api_key,model_name="qwen-2.5-coder-32b")

while True:
    user_input = input("You: ")
    if user_input == 'exit':
        break
    result = model.invoke(user_input)
    print('AI: ', result.content)