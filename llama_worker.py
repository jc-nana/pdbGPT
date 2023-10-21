from llama_index import Document
from llama_index import ServiceContext, get_response_synthesizer
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.llms import LangChainLLM
from llama_index.embeddings import LangchainEmbedding
from llama_index import VectorStoreIndex, GPTListIndex
from llama_index.composability import ComposableGraph
from langchain.llms import Cohere, AI21, OpenAIChat
from langchain.embeddings import CohereEmbeddings, OpenAIEmbeddings

class LlamaWorker:
    # embedding/llm api is a tuple (api_provider, api_key), e.g. ("openai", "your_api_key")
    def __init__(self, embedding_api, llm_api):
        self.embedding_api_provider, self.embedding_api_key = embedding_api
        self.llm_api_provider, self.llm_api_key = llm_api
        self.llm_embed = self._create_langchain_embedding(self.embedding_api_provider, self.embedding_api_key)
        self.llm_command = self._create_langchain_llm(self.llm_api_provider, self.llm_api_key)
        self.service_context = ServiceContext.from_defaults(embed_model=self.llm_embed,llm=self.llm_command)



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
    @staticmethod
    def _create_langchain_llm(api_provider, api_key):
        if api_provider == "Cohere":
            return LangChainLLM(llm=Cohere(model='command', cohere_api_key=api_key))
        if api_provider == "OpenAI":
            return LangChainLLM(llm=OpenAIChat(model='gpt-4', openai_api_key=api_key))
        if api_provider == "AI21":
            return LangChainLLM(llm=AI21(model='j2-ultra', ai21_api_key=api_key))
        raise ValueError(f"Unsupported llm api provider: {api_provider}")
        
    def create_query_engine(self, context_list):
        retriever = self.generate_retriever_from_publications(context_list)
        # configure response synthesizer
        response_synthesizer = get_response_synthesizer(
            response_mode="tree_summarize",
            service_context=self.service_context
        )
        # assemble query engine
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer
        )
        return query_engine

    def generate_retriever_from_publications(self, context_list):
        pub_index = self.generate_vector_index_from_publications(context_list)
        pub_retriever = VectorIndexRetriever(pub_index, service_context=self.service_context)
        return pub_retriever

    def generate_vector_index_from_publications(self, context_list):
        documents = [Document(text=context) for context in context_list]
        pub_index = VectorStoreIndex.from_documents(
            documents,
            service_context=self.service_context
        )
        return pub_index


        
"""
llm_embed  = LangchainEmbedding(langchain_embeddings=CohereEmbeddings(model='embed-multilingual-v2.0'))
# llm_command  = LangChainLLM(llm=Cohere(model='command'))
llm_command = LangChainLLM(llm=AI21(model='j2-ultra'))
service_context = ServiceContext.from_defaults(
    embed_model=llm_embed,
    llm=llm_command
)

def create_query_engine(context_list):
    retriever = generate_retriever_from_publications(context_list)
    # configure response synthesizer
    response_synthesizer = get_response_synthesizer(
        response_mode="tree_summarize",
        service_context=service_context
    )
    # assemble query engine
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer
    )
    return query_engine

def generate_retriever_from_publications(context_list):
    pub_index = generate_vector_index_from_publications(context_list)
    pub_retriever = VectorIndexRetriever(pub_index, service_context=service_context)
    return pub_retriever

def generate_vector_index_from_publications(context_list):
    documents = [Document(text=context) for context in context_list]
    pub_index = VectorStoreIndex.from_documents(
        documents,
        service_context=service_context
    )
    return pub_index

def generate_graph_from_publications():
    # graph = ComposableGraph.from_indices(
    #     GPTListIndex,
    #     [index_set[y] for y in years],
    #     [summaries[y] for y in years],
    #     service_context=service_context
    # )
    pass

def create_vectorstore_from(db, query, k=4):
    pass
"""