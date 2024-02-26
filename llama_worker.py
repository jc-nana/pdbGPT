from llama_index.core import Document, Settings
from llama_index.core import get_response_synthesizer
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.langchain import LangChainLLM
from llama_index.embeddings.langchain import LangchainEmbedding
from langchain_community.embeddings import CohereEmbeddings, OpenAIEmbeddings
from langchain_community.llms import cohere, ai21
from langchain_openai import ChatOpenAI


class LlamaWorker:
    # embedding/llm api is a tuple (api_provider, api_key), e.g. ("openai", "your_api_key")
    def __init__(self, embedding_api, llm_api):
        self.embedding_api_provider, self.embedding_api_key = embedding_api
        self.llm_api_provider, self.llm_api_key = llm_api
        self.llm_embed = self._create_langchain_embedding(
            self.embedding_api_provider, self.embedding_api_key)
        self.llm_command = self._create_langchain_llm()
        Settings.llm = self.llm_command
        Settings.embed_model = self.llm_embed
        self.service_context = Settings

    # currently only support OpenAI and Cohere

    @staticmethod
    def _create_langchain_embedding(api_provider, api_key):
        if api_provider == "Cohere":
            return LangchainEmbedding(
                langchain_embeddings=CohereEmbeddings(
                    model='embed-multilingual-v2.0', cohere_api_key=api_key))
        if api_provider == "OpenAI":
            return LangchainEmbedding(
                langchain_embeddings=OpenAIEmbeddings(
                    model='text-embedding-ada-002', openai_api_key=api_key))
        raise ValueError(f"Unsupported embedding api provider: {api_provider}")

    # currently only support OpenAI and Cohere
    def _create_langchain_llm(self):
        if self.llm_api_provider == "Cohere":
            return LangChainLLM(llm=cohere.Cohere(model='command', cohere_api_key=self.llm_api_key))
        if self.llm_api_provider == "OpenAI":
            return LangChainLLM(llm=ChatOpenAI(model='gpt-3.5-turbo-0125', openai_api_key=self.llm_api_key))
        if self.llm_api_provider == "AI21":
            return LangChainLLM(llm=ai21.AI21(model='j2-ultra', ai21_api_key=self.llm_api_key))
        raise ValueError(
            f"Unsupported llm api provider: {self.llm_api_provider}")

    def create_query_engine(self, context_list):
        retriever = self.generate_retriever_from_publications(context_list)
        # configure response synthesizer
        response_synthesizer = get_response_synthesizer(
            response_mode="tree_summarize",
        )
        # assemble query engine
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer
        )
        return query_engine

    def generate_retriever_from_publications(self, context_list):
        pub_index = self.generate_vector_index_from_publications(context_list)
        pub_retriever = VectorIndexRetriever(
            pub_index, service_context=self.service_context)
        return pub_retriever

    def generate_vector_index_from_publications(self, context_list):
        documents = [Document(text=context) for context in context_list]
        pub_index = VectorStoreIndex.from_documents(documents)
        return pub_index
