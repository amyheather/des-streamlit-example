"""Home page introducing the nurse clinic simulation."""

import streamlit as st

st.title("Nurse clinic simulation")

st.write("""
This app allows you to run a simple discrete-event simulation (DES) of a nurse
clinic.
""")

st.image("images/model_diagram.drawio.png")

st.caption("""
Model diagram: patient arrives, waits for an available nurse, has a
consultation, then leaves.
""")
