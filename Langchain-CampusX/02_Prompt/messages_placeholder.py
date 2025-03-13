## its play a big role in chat time like. today you are talking to bot and tomorrow came and start talking and MESSAGESPLACEHOLDER paly a role like its extract your previous messages and add into the new conversion so model can understand your progress.

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# chat template
chat_template = ChatPromptTemplate([
    ('system','You are a helpful customer support agent'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human','{query}')
])

chat_history = []
# load chat history
file = "./Langchain-CampusX/Prompt/chat_history.txt"
with open(file) as f:
    chat_history.extend(f.readlines())

print(chat_history)

# create prompt
prompt = chat_template.invoke({'chat_history':chat_history, 'query':'Where is my refund'})

print(prompt)

