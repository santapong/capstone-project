import os
import logging

from abc import abstractmethod
from dotenv import load_dotenv
from typing import List, Dict

from langchain_core.tools.simple import Tool
from langchain_core.output_parsers import StrOutputParser

from langchain.chat_models import init_chat_model
from langchain.tools.retriever import create_retriever_tool

from langchain_ollama import OllamaEmbeddings 
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

from langgraph.graph import END, StateGraph, START
from langgraph.graph.state import CompiledStateGraph

from capstone.backend.llms.core import RAGModel
from capstone.backend.llms.utils import register_tool
from capstone.backend.llms.prompts import (
    rag_prompt, 
    decision_prompt,
    re_write_prompt,
    refinement_prompt
    )
from capstone.backend.llms.models import (
    AgentState,
    GradeDocuments,
    ) 

from IPython.display import Image, display

# Parsing ENV parameter from .env
load_dotenv()
logging.getLogger(__name__)

# See Agent Paradigms
# https://github.com/santapong/CapStone-Project/blob/santapong/llms/imgs/Workflow_paradigm.png
# Agentic That have RAG and Google seacrh inside.
class AgenticModel(RAGModel):
    def __init__(self):
        
        # Using inheritance.
        super().__init__()
        
        # Init Model.
        self.llm = self.__init_model()
        self.vector_store =  self.get_vector_store()
        
        # Setting Tool Parameter for Decorator.
        self.__tool_methods = [
            method_name for method_name in dir(self)
            if callable(getattr(self, method_name)) and hasattr(getattr(self, method_name), "_is_tool")
        ]
        
        # Setting Embedding model.
        self.embedding = OllamaEmbeddings(
            model=os.getenv("EMBEDDING_MODEL", default='bge-m3'),
            base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434")
        )
        
    # Intialize Model internal method
    def __init_model(
            self,
            llm_model:str = os.getenv("LLM_MODEL"),
            model_provider:str = os.getenv("MODEL_PROVIDER"),
            temperature: float = os.getenv("TEMPERATURE"),
            model_base_url: str = os.getenv("MODEL_BASE_URL")
        ):
        return init_chat_model(
                model=llm_model, 
                model_provider=model_provider, 
                temperature=temperature,
                base_url=model_base_url,
            )   
        
    # Not use
    # RAG model tool.
    @register_tool
    def retriever_tool(self)-> Tool:
        tool = create_retriever_tool(
            retriever=self.retriever,
            name="RAG tools",
            description="Use to retrived document about Automation Engineering in KMITL.",
        )
        
        return tool
    
    # Search tool Using Duckduckgo search.
    @register_tool
    def duckduckgo(self)->DuckDuckGoSearchRun:
        wrapper = DuckDuckGoSearchAPIWrapper(max_results=15)
        tool = DuckDuckGoSearchRun(
            name="Websearh tool from Duckduckgo",
            description="Use to search website via Duckduckgo.",
            api_wrapper=wrapper,
        )
        
        return tool
    
    # Google search method.
    def google_search(
        self,
        query,
        top_k,
        ):
        
        # Get API Wrapper from Google
        wrapper = GoogleSearchAPIWrapper(
            google_cse_id=os.getenv("GOOGLE_CSE_ID"), # Custom Search Engine ID
            google_api_key=os.getenv("GOOGLE_API_KEY"), # Google API KEY
        )
        
        # lambda function to create list of document
        result = lambda query, top_k: list(wrapper.results(query=query, num_results=top_k))
        links = [
            result["link"] for result in result(query=query, top_k=top_k) 
        ]
        
        # Load Document from links.
        documents = WebBaseLoader(web_paths=links).load()
        
        return documents
        
        
    # Abstract to collect tool inside AgenticModel class.
    @abstractmethod
    def get_tools(self) -> List:
        """Collect tools from AgenticModel"""
        return [getattr(self, method_name)() for method_name in self.__tool_methods]
    
    ## Node

    # NOTE: Pass
    # Using to grading the document that retrive.
    def grade_document(
            self, 
            state: AgentState
        )-> Dict[str, any]:
        """
        
        """
        logging.info("---- Grading ----")
        
        # Get question from AgentState
        question = state["question"]
        documents = state["documents"]
        
        # Set structure of output > yes or no.
        structured_llm_grader = self.llm.with_structured_output(GradeDocuments)
        
        # Grader Chain
        retrieval_grader = decision_prompt | structured_llm_grader # This format call LCEL (LangChain Expression Language)
        
        # Result expected {"binary_score": "yes"}
        response = retrieval_grader.invoke({"question": question, "context": documents})
        
        return {"web_search": response}

    # NOTE: Pass
    # Retrieval Agent using ChromaDB.
    def retrieval_agent(
            self, 
            state: AgentState
        )-> Dict[str, any]:
        logging.info("----Retrieve Agent----")
        print("Retrieval")
        # Get question from Agentstate
        question = state["question"]
    
        # Retrieval
        documents = self.vector_store.similarity_search_with_score(
            query=question,
            k=13
        )
        
        return {"documents": documents, "question": question}
    
    # NOTE: pass
    # Using too rewrite the question to search the website.
    def rewrite(
            self,
            state: AgentState,
        )-> Dict[str, any]:
        
        logging.info("----- Rewrite -----")
        print("Rewrite")
        # Parsing the Question from AgentState
        question = state["question"]
        
        # LLM Chains
        rewriter =  re_write_prompt | self.llm | StrOutputParser() # This format call LCEL (LangChain Expression Language)
        
        # rewrite question from LLM.
        rewrite_question =  rewriter.invoke({"question":question})
        
        return {"rewrite": rewrite_question}

    # NOTE: Pass
    # Search Agent using Google search.
    def search_agent(
            self, 
            state: AgentState 
        )-> Dict[str, any]:
        logging.info("---Using Google search---")
        print("search")
        
        # Parsing key from AgentState
        question = state["question"]
        web_result = []
        
        # Using Google Search.
        documents = self.google_search(query=question, top_k=3)
        web_result.append(documents)
        
        return {"web_result": web_result}
        
    # NOTE: Pass
    # Generate Agent.
    def generate_agent(
            self, 
            state: AgentState
        )-> Dict[str, any]:
        logging.info("---Using Generate---")
        
        # Parsing key from AgentState.
        question = state["question"]
        web_search: GradeDocuments = state["web_search"]
        
        # Rag_chain
        rag_chain = rag_prompt() | self.llm | StrOutputParser() # This format call LCEL (LangChain Expression Language)
        
        # Select Document to asking.
        if web_search.binary_score == "yes":
            # If using RAG only will get document.
            logging.info("----Using RAG.----")
            documents = state["documents"]
            filled_document: List[str] = documents
            
        elif web_search.binary_score == "no":
            # If document not sufficient to Answer it will Add more search result to answer.
            logging.info("----Using Search.----")
            web_result = state["web_result"]
            filled_document: List[str] = web_result

        # Query To LLM
        response = rag_chain.invoke({"context": filled_document, "question":question})
        
        return {"generation": response}
        
    # Refined Agent
    def refined_agent(
            self, 
            state: AgentState
        )-> Dict[str, any]:
        
        logging.info("---- Refined ----")
        
        # Parsing key from AgentState.
        generation = state["generation"]
        
        # LLM Chain
        refined_chain = refinement_prompt | self.llm | StrOutputParser() # This format call LCEL (LangChain Expression Language)
        
        # Get Answer from LLM
        response = refined_chain.invoke({"generation":generation})
        
        return {"refine": response}
    
    ## Edge
        
    # NOTE: pass
    # Get decision from Grade_document. 
    def decide_to_search(
            self,
            state: AgentState
        )-> str:
        
        """
        Using for decide to search or go generate
        
        return: 'yes' or 'no'
        """
        
        # Parsing key from AgentState.
        web_search: GradeDocuments = state["web_search"]
        
        # Decide to search or not
        if web_search.binary_score == "yes":
            return "yes"
        elif web_search.binary_score == "no":
            return "no"
        
    
# Reference
# https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_crag/
# Create Garph using inheritance to AgenticModel.
class Garph(AgenticModel):
        def __init__(self):
            super().__init__()
            
        # Compile workflow here.
        @abstractmethod
        def compile(self)-> CompiledStateGraph:
            # Set StateGraph
            self.workflow = StateGraph(AgentState)
            
            # Build Node
            self.workflow.add_node("retrieval_agent", self.retrieval_agent)
            self.workflow.add_node("grade_document", self.grade_document)
            self.workflow.add_node("rewriter_agent", self.rewrite)
            self.workflow.add_node("search_agent", self.search_agent)
            self.workflow.add_node("generate_agent", self.generate_agent)
            self.workflow.add_node("refined_agent", self.refined_agent)
            
            
            # Build Graph using Edge to connect node to node.
            self.workflow.add_edge(start_key=START, end_key= "retrieval_agent")
            self.workflow.add_edge(start_key="retrieval_agent", end_key="grade_document")
            self.workflow.add_conditional_edges(
                source="grade_document", 
                path=self.decide_to_search,
                path_map={
                    "yes":"generate_agent",
                    "no":"rewriter_agent",
                })
            self.workflow.add_edge(start_key="rewriter_agent", end_key="search_agent")
            self.workflow.add_edge(start_key="search_agent", end_key="generate_agent")                        
            self.workflow.add_edge(start_key="generate_agent", end_key="refined_agent")
            self.workflow.add_edge(start_key="refined_agent", end_key=END)
            
            return self.workflow.compile()
        
        @abstractmethod
        def display(self):
            try:
                return display(Image(self.compile().get_graph(yray=True).draw_mermaid_png()))
            except Exception:
                pass

def get_agent():
    yield Garph().compile()

if __name__ == "__main__":
    import time
    from pprint import pprint
    test = Garph()
    start_time = time.time()    
    answer = test.compile().invoke({"question":"หลักสูตรออโตเมชันที่น่าสนใจ"})
    time_usage = time.time() - start_time
    pprint(f"time_usage = {time_usage}")
    pprint(f"Question: {answer['question']}")
    # pprint(f"rewrite: {answer['rewrite']}")
    pprint(f"Answer: {answer['generation']}")
    pprint(f"Refined: {answer['refine']}")
    # pprint(f"Documents: {answer['documents']}")
    # pprint(f"Web_result: {answer['web_result']}")