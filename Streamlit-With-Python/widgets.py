import streamlit as st
import pandas as pd

st.title("Streamlit Text Input")

name = st.text_input("Enter your name:")

age = st.slider("Select your age:", 0, 50, 25)

st.write(f"Your age is: {age}")

if name:
    st.write(f"Assalamualikum {name}")
    

# select Box

options = ['Python', 'java', 'assembely', 'CPP', 'Js']
choice = st.selectbox('Choose your favorite Progamming Langauge:',options=options)
st.write(f"You Selected {choice}")


data = {
    "Name" : ['Al Amin', 'Mohimen Azad', 'Aminul Islam'],
    'Age': [24, 22, 20],
    'Location': ['B-Block','I-Block', 'Jatra-bari' ]
}
df = pd.DataFrame(data=data)
# df.to_csv('sampledata.csv')
st.write(df)

## Upload Files
upload_file = st.file_uploader('Choose a CSV File', type='csv')

if upload_file is not None:
    df = pd.read_csv(upload_file)
    st.write(df)