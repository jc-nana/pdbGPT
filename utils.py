# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import inspect
import textwrap
from typing import List, Dict
import streamlit as st


# CSS styling
css = """
    .rounded-text {
        background-color: #404040;
        border-radius: 10px;
        padding: 5px;
        display: inline;
    }
"""

# Apply the CSS styling
# st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# # Display the rounded text
# st.markdown('<span class="rounded-text">Hello, World!</span>', unsafe_allow_html=True)


def show_code(demo):
    """Showing the code of the demo."""
    show_code = st.sidebar.checkbox("Show code", True)
    if show_code:
        # Showing the code of the demo.
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))

def parse_ebi_publication_list(pub_list: List[Dict]):
    parsed_dict = {}
    for i, pub_dict in enumerate(pub_list):
        parsed_dict[pub_dict['title']] = {
            'doi': pub_dict['doi'],
            'abstract': pub_dict['abstract'],
            'primary': i == 0
        }
    return pub_list[0]['title'], parsed_dict

# currently only extract information for primary citation, TODO: integrate with pubmed API to get all citations
def parse_rcsb_publication_dict(entry_response: Dict, pubmed_response: Dict):
    parsed_dict = {}
    citations = entry_response['citation']
    primary_citation = [pub for pub in citations if pub["id"]=="primary"][0]
    parsed_dict[primary_citation["title"]] = {
        'doi': pubmed_response['rcsb_pubmed_doi'],
        'abstract': {"abstract": pubmed_response['rcsb_pubmed_abstract_text']},
        'primary': True
    }
    return primary_citation["title"], parsed_dict

def render_publication(title: str, content: Dict, primary_pub_title: str):
    st.markdown(f"### {title}")
    if primary_pub_title == title:
        # Display the rounded text
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
        st.markdown('<span class="rounded-text">Primary Citation</span>', unsafe_allow_html=True)
    if content['doi'] is None:
        st.markdown(f"doi: To be published.")
    else:
        st.markdown(f"doi: [{content['doi']}](https://doi.org/{content['doi']})")
    for assignment, text in content['abstract'].items():
        if text is not None:
            st.markdown(f"###### {assignment}")
            st.text(textwrap.fill(text, width=80))

            