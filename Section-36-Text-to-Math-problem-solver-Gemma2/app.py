import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMMathChain, LLMChain
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from dotenv import load_dotenv
from langchain.callbacks import StreamlitCallbackHandler


## Set up the Steamlit app
st.set_page_config(page_icon="🧮", page_title="Text to Math Problem Solver and Data Search Assistant")
st.title("Text to Math problem solver Using Google Gemma 2")

groq_api_key = st.sidebar.text_input(label="Greq Api Key", type="password")

if not groq_api_key:
    st.info("Please add your groq Api key to continue")
    st.stop()

llm=ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

## Initializing the tools
wikipedia_wrapper=WikipediaAPIWrapper()
wikipedia_tool=Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the internet to find the various information on the topics mentioned"
)

## Initialize th math tools

math_chain = LLMMathChain.from_llm(llm=llm)
calculator=Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tools for answering math related questions. only input mathematical expression need to be provided"
    
)

prompt="""
Your a agent tasked to solving userrs math
"""