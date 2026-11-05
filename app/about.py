import streamlit as st

st.title("About")

with st.expander(label="What is the source of this model?"):
    st.write("""
This is a synthetic model created for the HSMA course. It is from
[session 2B: Introduction to SimPy](https://docs.google.com/presentation/d/1Hf7aAHQAg9ULrk7zco03lwUn3qlwcAjDrpBXqaGcsSY/edit?usp=sharing).
""")
