from typing import Any

import numpy as np

import streamlit as st
from streamlit.hello.utils import show_code


def pdb_gpt_demo() -> None:
    pdb_id = st.sidebar.text_area("Input PDB ID to query about:")

    # Non-interactive elements return a placeholder to their location
    # in the app. Here we're storing progress_bar to update it later.
    progress_bar = st.sidebar.progress(0)

    # These two elements will be filled in later, so we create a placeholder
    # for them using st.empty()
    frame_text = st.sidebar.empty()
    image = st.empty()

    # We clear elements by calling empty on them.
    progress_bar.empty()
    frame_text.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


st.set_page_config(page_title="PDB GPT", page_icon="🧬")
st.markdown("# PDB GPT")
st.sidebar.header("PDB GPT")

pdb_gpt_demo()

show_code(pdb_gpt_demo)
