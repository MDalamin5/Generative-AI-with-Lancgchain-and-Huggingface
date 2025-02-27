
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, load_prompt

groq_api_key=os.getenv("GROQ_API_KEY")

model=ChatGroq(groq_api_key=groq_api_key,model_name="qwen-2.5-coder-32b")

st.header("Research Tool")

## take some input form sidebar
st.sidebar.title("Select your input Parameter")
paper_input = st.sidebar.selectbox( "Select Research Paper Name", ["Attention Is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis"] )

style_input = st.sidebar.selectbox( "Select Explanation Style", ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"] ) 

length_input = st.sidebar.selectbox( "Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"] )

template = load_prompt('template.json')

# prompt = template.invoke(
#     {
#         'paper_input': paper_input,
#         'style_input': style_input,
#         'length_input': length_input
#     }
# )

# print(user_input)
if st.button("Summarize"):
    chain = template | model
    result = chain.invoke(
      {
        'paper_input': paper_input,
        'style_input': style_input,
        'length_input': length_input
    }  
    ) 
    st.write(result.content)
