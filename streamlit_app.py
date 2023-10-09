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

import textwrap
from PDB_GPT import pdb_gpt
from llama_worker import LlamaWorker
import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="PDB GPT",
        page_icon="🧬",
        initial_sidebar_state="collapsed"
    )

    st.write("# PDB GPT")

    st.markdown(
        """
         PDB GPT lets you query a PDB id, and ask an LLM to read its related publication to answer your questions about the protein in the entry, or any molecules in the entry!
    """
    )
    openai_key = st.text_input("🤖 Input your OpenAI API key for best experience:")
    st.info(icon="ℹ️", body="Providing an OpenAI API key will improve your experience of the app. By default, this app uses a rate-limited Cohere API or AI21 API.")

    if openai_key:
       lw = LlamaWorker(
          embedding_api=("OpenAI", openai_key), 
          llm_api=("OpenAI", openai_key))
    else:
       lw = LlamaWorker(
          embedding_api=("Cohere", st.secrets["COHERE_API_KEY"]), 
          llm_api=("AI21", st.secrets["AI21_API_KEY"]))

    query_text = st.empty()
    col1, col2 = st.columns(2)

    with col1:
      query = st.text_input("#### Enter question to ask about this PDB entry using the selected publication as context.")
      respose = st.empty()
      example_query = "What molecules are of interest?"
      st.markdown(f"###### Example Query: {example_query}")
      example_response = st.empty()
    context_list = pdb_gpt(col1, col2, query_text)
        
    query_engine = lw.create_query_engine(context_list)
    example_response.markdown(f"*{query_engine.query(example_query)}")
    if query:
      respose.markdown(f"*{query_engine.query(query)}")


if __name__ == "__main__":
    run()
