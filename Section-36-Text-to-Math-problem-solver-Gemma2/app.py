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
Your a agent tasked to solving users mathemtical questions. Logically arrive at the solution and provide a detailed explanation and display it point wise for the question below \n 
Question: {question}
Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)


## combine all the tools into chain
chain = LLMChain(llm=llm, prompt=prompt_template)


reasoning_tool = Tool(
    name="Reasoning tool",
    func=chain.run,
    description="A tool for answering logic-based and reasoning question."
)

## initalize the agents
assistant_agent=initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_error=True
)

if "messages" not in st.session_state:
    st.session_state['messages']=[
        {"role":"assistant", "content":"Hi, i'm Math chatbot who can answer all your math questions."}
    ]
    
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])
    
## function to generate the response
# def generate_response(question):
#     response=assistant_agent.invoke({"input":question})
#     return response


## lets start the interaction
question=st.text_area("Enter your question:","How to add tow number which is int and double")


if st.button("Find my answer"):
    if question:
        with st.spinner("Generate Response..."):
            st.session_state.messages.append({"role":"user","content":question})
            st.chat_message("user").write(question)
            
            st_cb=StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = assistant_agent.run(st.session_state.messages, callbacks=[st_cb])
            
            st.session_state.messages.append({"role":'assistant',"content":response})
            st.write("### Response:")
            st.success(response)
    else:
        st.write("Please Enter your question")
            
            