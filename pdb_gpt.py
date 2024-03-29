from typing import List, Dict
import requests
import streamlit as st
import utils


def get_pdb_publications(pdb_id: str) -> Dict:
    try:
        pub_dicts_list = get_pdb_publications_from_ebi(pdb_id)
        pimary_title, pubs_dict = utils.parse_ebi_publication_list(pub_dicts_list)
    except Exception:
        try:
            entry_response, pubmed_response = get_pdb_publications_from_rcsb(pdb_id)
            pimary_title, pubs_dict = utils.parse_rcsb_publication_dict(entry_response, pubmed_response)
        except:
            raise Exception("get_pdb_publications failed for both rcsb and ebi")
    return pimary_title, pubs_dict

def get_pdb_publications_from_rcsb(pdb_id: str) -> List[Dict]:
    pubmed_query = f"https://data.rcsb.org/rest/v1/core/pubmed/{pdb_id}"
    pubmed_response = requests.get(pubmed_query)
    entry_query = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    entry_response = requests.get(entry_query)
    if pubmed_response.status_code != 200 or entry_response.status_code != 200:
        raise Exception(f'get_pdb_publication_from_rcsb({pdb_id}) get request failed with status pubmed: {pubmed_response.status_code}, entry: {entry_response.status_code}')
    return (entry_response.json(), pubmed_response.json())



def get_pdb_publications_from_ebi(pdb_id: str) -> List[Dict]:
    pdb_id = str.lower(pdb_id)
    base_url = "https://www.ebi.ac.uk/pdbe/api/pdb/entry/publications/"
    response = requests.get(f"{base_url}{pdb_id}")
    if response.status_code != 200:
        raise Exception(f'get_pdb_publication_from_ebi({pdb_id}) get request failed with status {response.status_code}')
    pub_dicts = response.json()[pdb_id]
    return pub_dicts



def pdb_gpt(_col1, _col2, _query_text) -> List[str]:
    pdb_id = _query_text.text_input("Input PDB ID to query about: (e.g. 1cbs, 125L)",
                                    "1cbs")
    pdb_id = pdb_id.strip()
    context_list = []

    progress_bar = st.sidebar.progress(0)
    if pdb_id:
        with _col2:
            st.markdown("#### Publications")
            # pub_dicts_list = get_pdb_publications_from_ebi(pdb_id)
            primary_pub_title, pubs_dict = get_pdb_publications(pdb_id)
            # primary_pub_title = pub_dicts_list[0]['title']
            # make sure primary publication is correctly retrieved
            assert pubs_dict[primary_pub_title]['primary']
            select_pub = st.selectbox(label='Select publication to view', options=pubs_dict.keys())
            utils.render_publication(select_pub, pubs_dict[select_pub], primary_pub_title)
        with _col1:
            st.markdown("#### Select publication to use as context for LLM.")
            for title, content in pubs_dict.items():
                if st.checkbox(label=title, value=content['primary']):
                    context_list.append(title)
                

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")
    return context_list, pdb_id

