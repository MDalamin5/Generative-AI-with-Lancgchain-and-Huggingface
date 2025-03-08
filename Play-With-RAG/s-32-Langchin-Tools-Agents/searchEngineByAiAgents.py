import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun, DuckDuckGoSearchResults, TavilySearchResults
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler



arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=300)
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

wiki_wapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=300)
wiki = WikipediaQueryRun(api_wrapper=wiki_wapper)

search = DuckDuckGoSearchResults(name="search")

st.title("🔎 LangChain - Chat with search")
"""
In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
"""

## sidebar
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your GroQ API key:", type='password')

## Implement Chat history
if 'messages' not in st.session_state:
    st.session_state["messages"]=[
        {
            "role":"assistant",
            "content":"Assalamualikum, I'm a chatbot who can search in the web. How can i help you today?"
        }
    ]
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])
    
if prompt:=st.chat_input(placeholder="What is Prompt Engineering and why should Learn it?"):
    st.session_state.messages.append(
        {
            'role':'user',
            'content':prompt
        }
    )
    st.chat_message("user").write(prompt)
    
    
    ## load llm
    llm = ChatGroq(groq_api_key=api_key, model_name='qwen-2.5-32b', temperature=0.5, streaming=True)
    tools=[search, arxiv, wiki]
    
    search_agent=initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handling_parsing_errors=True)
    # ZERO_SHOT_REACT_DESCRIPTION is when agents talk each other its do not check the previous chat history based on current input only.
    # CHAT_ZERO_SHOT_REACT_DESCRIPTION is when agents talk each other its do check the previous chat history and based on current input.
    
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response=search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append(
            {
                'role':"assistant",
                'content':response
            }
        )
        st.write(response)
    