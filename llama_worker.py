from llama_index import Document
from llama_index import ServiceContext, get_response_synthesizer
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.llms import LangChainLLM
from llama_index.embeddings import LangchainEmbedding
from llama_index import VectorStoreIndex, GPTListIndex
from llama_index.composability import ComposableGraph
from langchain.llms import Cohere, AI21
from langchain.embeddings import CohereEmbeddings

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
