import os
import logging

from uuid import uuid4
from typing import (
    List, 
    Union, 
    Dict,
    )

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaEmbeddings 
from langchain_core.documents import Document
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter

from capstone.backend.llms.prompts import (
    rag_prompt,
    )

logging.getLogger(__name__)

# Get from ENV
LLM_MODEL = os.getenv("LLM_MODEL",default= "llama3.2")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL",default='bge-m3')
COLLECTION_NAME = os.getenv("COLLECTION_NAME",default="langchain")
MODEL_BASE_URL = os.getenv("MODEL_BASE_URL")
API_KEY = os.getenv("TYPHOON_API_KEY")

# Persist Directory
PERSIST_DIR = os.getenv("PERSIST_DIR",default="database/vector_history")


# Need to change the name to Vector Database
# RAG Class model.
class RAGModel:
    def __init__(
            self,
            temperature: float = 0.5
            ):
        self.__vector_store = self.__chroma_connect()
        self.__llm = ChatOpenAI(
            base_url=MODEL_BASE_URL,
            model=LLM_MODEL,
            api_key=API_KEY,
            max_completion_tokens=8192,
            temperature=temperature,
        )

    def get_vector_store(self):
        return self.__vector_store

    def __chroma_connect(self):
        ollama_base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        return Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=ollama_base_url),
            persist_directory=PERSIST_DIR
            # **client_settings
            )

    # Internal Split Text
    def __split_text(self,
                    metadatas,
                    contents:str,
                    chunk_size:int = 4096,
                    separaters: str ='/n',
                    ):
        
        # Splitter text API contents.
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_size*0.25,
            separators=separaters
            )
        texts =  splitter.split_text(contents)
        
        # Generate Metadata
        generate_metadata = [ metadatas[0] for _ in range(len(texts)) ]
        
        # Create Document from Text.
        documents = splitter.create_documents(
            texts=texts,
            metadatas=generate_metadata
            )

        return documents

    # Load Document From API
    async def aload_from_API(self,
                  metadatas,
                  contents:Union[Dict[str,str],str],
                  )-> List[Document]:
        
        # Split text from API
        documents = self.__split_text(
            contents=contents,
            metadatas=metadatas
            )
        
        # Add Metadata for documents.
        ids = [str(uuid4()) for _ in range(len(documents))]
        
        # Add Document to Vector store.
        metadata = self.__vector_store.add_documents(
            documents=documents,
            ids=ids
            )

        return metadata

    # Query to LLMs.
    def invoke(
            self, 
            question:str,
            ):

        # Call Retriever
        self.retriever = self.__vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                'k': 15,
                "lambda_mult":0.1,
                "fetch_k":30,
                }
            )

        # Create Chains
        combine_docs_chain = create_stuff_documents_chain(
            prompt=rag_prompt(),
            llm=self.__llm
        )

        # Create Retrieval Chains
        retrieval_chains = create_retrieval_chain(
            retriever=self.retriever,
            combine_docs_chain=combine_docs_chain
            )

        return retrieval_chains.invoke({"question": question,"input":question})

# Make for FastAPI Depends 
def get_RAG():
    yield RAGModel()

if __name__ == '__main__':
    test = RAGModel()
    vector_store = test.get_vector_store()