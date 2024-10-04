import streamlit as st
import pandas as pd
import numpy as np

## Title of the application

st.title("Assalamualikum")

## Display s Simple Text
st.write('This is a simple Text')

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column' : [10, 20, 30, 40]
})

# display the Dataframe
st.write("This the first DataFrame")
st.write(df)

chart_data = pd.DataFrame(
    np.random.randn(20, 3), columns=['a', 'b', 'c']
)
st.line_chart(chart_data)