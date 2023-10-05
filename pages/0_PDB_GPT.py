from typing import Any
import utils
import textwrap
import numpy as np
import requests
from typing import List, Dict
import streamlit as st

# layout
st.set_page_config(page_title="PDB GPT", page_icon="🧬")
st.markdown("# PDB GPT")
st.sidebar.header("PDB GPT")
query_text = st.empty()
col1, col2 = st.columns(2)

def get_pdb_publications(pdb_id: str) -> List[Dict]:
    pdb_id = str.lower(pdb_id)
    base_url = "https://www.ebi.ac.uk/pdbe/api/pdb/entry/publications/"
    response = requests.get(f"{base_url}{pdb_id}")
    if response.status_code != 200:
        raise Exception(f'get_pdb_publication({pdb_id}) get request failed with status {response.status_code}')
    pub_dicts = response.json()[pdb_id]
    return pub_dicts



def pdb_gpt() -> None:
    pdb_id = st.sidebar.text_area("Input PDB ID to query about:")
    pdb_id = pdb_id.strip()

    progress_bar = st.sidebar.progress(0)
    if pdb_id:
        query_text.markdown(f"### Query: {pdb_id}")
        with col2:
            st.markdown(f"## Publications")
            pub_dicts_list = get_pdb_publications(pdb_id)
            pubs_dict = utils.parse_publication_list(pub_dicts_list)
            primary_pub_title = pub_dicts_list[0]['title']
            # make sure primary publication is correctly retrieved
            assert pubs_dict[primary_pub_title]['primary']
            select_pub = st.selectbox(label='Select publication to view', options=pubs_dict.keys())
            utils.render_publication(select_pub, pubs_dict[select_pub], primary_pub_title)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    
    st.button("Re-run")

pdb_gpt()
