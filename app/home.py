"""Home page introducing the nurse clinic simulation."""

import streamlit as st

st.title("Nurse clinic simulation")

st.write("""
This app allows you to run a simple discrete-event simulation (DES) of a nurse
clinic.

This is a synthetic model created for the HSMA course. It is from
[session 2C: Replications, Reproducibility and Multiple Activities](https://docs.google.com/presentation/d/1ZCgLD82pcPGyNPMvpki724URyNudy_CNpLn882V9B1w/edit?usp=sharing).
""")

st.image("images/model_diagram.drawio.png")

st.caption("""
Model diagram: patient arrives, waits for an available nurse, has a
consultation, then leaves.
""")
