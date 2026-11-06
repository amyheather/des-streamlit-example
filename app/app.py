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
        st.Page("simulation.py", title="Run simulation"),
        st.Page("results.py", title="View results"),
    ]
)
pg.run()

# ----------------------------------------------------------------------------
# Session state set-up
# ----------------------------------------------------------------------------
# Doing it here as otherwise if click straight on view results get error

if "scenarios" not in st.session_state:
    st.session_state.scenarios = {}
