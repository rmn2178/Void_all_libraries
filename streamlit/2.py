import streamlit as st
import datetime

st.title("Hello World")
st.header("Main header")
st.subheader("Main subheader")

pressed = st.button("press me")

if pressed:
    print("The button was pressed")
else:
    print("The button was not pressed")

st.markdown("This is markdown")
st.markdown("This is _markdown_")
st.markdown("This is ***markdown***")

st.caption("This is _caption_")

code_line = """
for i in range(0,len(array):
    print(array[i])
"""
st.code(code_line, language="python")

st.date_input("Date", datetime.datetime.now())