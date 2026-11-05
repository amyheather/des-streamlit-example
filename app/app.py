"""Entrypoint for app. Configures app and defines navigation."""

import streamlit as st

# Configure default settings for the app
st.set_page_config(
    page_title="Nurse clinic DES",
    page_icon="🏥",
)

# Add logo to sidebar
st.logo(
    image="images/nihr_logo.png",
)

# Define pages and their order
pg = st.navigation(
    [
        st.Page("home.py", title="Home"),
        st.Page("simulation.py", title="Simulation"),
        st.Page("about.py", title="About"),
    ]
)
pg.run()
