import validators, streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from langchain_huggingface import HuggingFaceEndpoint
import os
## streamlit app

st.set_page_config(page_title="LangChain: Summarize Text from YT or Website", page_icon="🦜️")
st.title("🦜️ LangChain: Summarize Text from YT or Website")
st.subheader("Summarize URL")

## get greq api key and url field to be summarized

with st.sidebar:
    hf_api_key=st.text_input("Hugging Face API KEY", value="", type="password")

generic_url=st.text_input("URL", label_visibility="collapsed")

#model from Huggingface

repo_id="mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(repo_id=repo_id, max_length=150, temperature=0.6, token=hf_api_key)

# llm = ChatGroq(model="Gemma-7b-It", groq_api_key=groq_api_key)

prompt_template="""
provide a summary of following conten in 300 words:
Content:{text}
"""

prompt=PromptTemplate(template=prompt_template, input_variables=['text'])


if st.button("Summarize the Content from YT or Website"):
    ## validate all inputs
    if not hf_api_key.strip() or not generic_url.strip():
        st.error("Please provide th information to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid url. it can my be ty video link or web url")
    else:
        try:
            with st.spinner("Waiting..."):
                if "youtube.com" in generic_url:
                    loader=YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url], ssl_verify=False, header={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                docs=loader.load()
                
                ## Chain for summarization
                chain=load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary=chain.run(docs)
                
                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception: {e}")