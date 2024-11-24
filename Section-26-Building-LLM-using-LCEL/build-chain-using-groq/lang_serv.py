from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
from langserve import add_routes

groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(model="gemma2-9b-it", groq_api_key = groq_api_key)

## Prompt Template
generic_template = "Translate the following into {language}"
prompt = ChatPromptTemplate.from_messages([
    ("system", generic_template), 
    ("user", "{text}")
])

parser = StrOutputParser()

## create chain
chain = prompt|model|parser

## App definition
app=FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API server using Langchain runnable interface"
)

add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
