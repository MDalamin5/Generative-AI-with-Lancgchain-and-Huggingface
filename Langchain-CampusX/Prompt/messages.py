from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

groq_api_key=os.getenv("GROQ_API_KEY")

model=ChatGroq(groq_api_key=groq_api_key,model_name="qwen-2.5-coder-32b")

messages=[
    SystemMessage(content="Your are a helpful assistant"),
    HumanMessage(content="Tell me about Langchain")
]

result = model.invoke(messages)
messages.append(AIMessage(content=result.content))
print(messages)