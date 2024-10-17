import os
import streamlit as st
import datetime
import logging
import re
import json
from typing import List, Dict, Any, Annotated
from langchain.schema import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import load_prompt, PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter, TextSplitter
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from utils.helpers import get_custom_font_css
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.runnables import RunnableParallel
from operator import itemgetter
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
import traceback

# LangSmith 
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "sigenie"


# Logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Constants
PDF_PATH = "./document/CHERRYShippingLineCompanyPolicy.pdf"
VECTOR_STORE_PATH = "./vector/compliance_faiss_index"
LAST_UPDATE_FILE = f"{VECTOR_STORE_PATH}/last_update.txt"

# Ensure necessary directories exist
os.makedirs(VECTOR_STORE_PATH, exist_ok=True)

# Set up OpenAI API
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings()

# Initialize OpenAI LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# Load the prompt
rag_prompt = load_prompt("prompts/compliance_rag_prompt.yaml")

# Create the chain
rag_chain = rag_prompt | llm | StrOutputParser()

# Global variable for vectorstore
global_vectorstore = None

# Helper functions for FAISS index and last update time
def save_faiss_index(vectorstore):
    vectorstore.save_local(VECTOR_STORE_PATH)

def load_faiss_index():
    if os.path.exists(VECTOR_STORE_PATH):
        return FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
    return None

def save_last_update(last_update):
    with open(LAST_UPDATE_FILE, "w") as f:
        f.write(last_update.isoformat())

def load_last_update():
    if os.path.exists(LAST_UPDATE_FILE):
        with open(LAST_UPDATE_FILE, "r") as f:
            return datetime.datetime.fromisoformat(f.read().strip())
    return datetime.datetime.min

def load_documents(sources: list[str]) -> list[Document]:
    docs = []
    for source in sources:
        if source.endswith('.pdf'):
            loader = PyPDFLoader(source)
            loaded_docs = loader.load()
            for doc in loaded_docs:
                doc.metadata['source'] = f"{source} (Page {doc.metadata['page']})"
            docs.extend(loaded_docs)
        else:
            raise ValueError(f"Unsupported source type: {source}")
    return docs

def check_pdf_update():
    last_update = load_last_update()
    pdf_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(PDF_PATH))
    return pdf_modified_time > last_update

class PolicySplitter(TextSplitter):
    def split_text(self, text: str) -> List[str]:
        pattern = r"CHERRY Shipping Line:?\s*(.+?)\s*-\s*Requirements and Restrictions"
        sections = re.split(pattern, text)
        chunks = []
        
        # First chunk is the comprehensive policy
        if sections[0].strip():
            chunks.append(sections[0].strip())
        
        # Process country-specific policies
        for i in range(1, len(sections), 2):
            if i+1 < len(sections):
                country = sections[i].strip()
                content = sections[i+1].strip()
                chunk = f"CHERRY Shipping Line: {country} - Requirements and Restrictions\n\n{content}"
                chunks.append(chunk)
        
        return chunks

def update_faiss_index():
    documents = load_documents([PDF_PATH])
    
    # Use the custom PolicySplitter
    policy_splitter = PolicySplitter()
    doc_splits = []
    
    for doc in documents:
        splits = policy_splitter.split_text(doc.page_content)
        for i, split in enumerate(splits):
            metadata = doc.metadata.copy()
            metadata['chunk'] = i
            doc_splits.append(Document(page_content=split, metadata=metadata))
    
    vectorstore = FAISS.from_documents(doc_splits, embeddings)
    save_faiss_index(vectorstore)
    save_last_update(datetime.datetime.now())
    return vectorstore

def initialize_vector_db():
    if st.session_state.vectorstore is None:
        st.info("Initializing Vector DB...")
        try:
            if os.path.exists(os.path.join(VECTOR_STORE_PATH, "index.faiss")):
                st.session_state.vectorstore = load_faiss_index()
                st.info("Existing Vector DB loaded.")
            else:
                st.warning("Vector DB not found. Creating a new one...")
                st.session_state.vectorstore = update_faiss_index()
                st.success("New Vector DB created successfully!")
        except Exception as e:
            st.error(f"Failed to initialize Vector DB: {e}")
            st.session_state.vectorstore = None
    
    if st.session_state.vectorstore is not None and check_pdf_update():
        st.warning("PDF has been updated. Updating Vector DB...")
        try:
            st.session_state.vectorstore = update_faiss_index()
            st.success("Vector DB updated successfully!")
        except Exception as e:
            st.error(f"Failed to update Vector DB: {e}")

def initialize_session_state():
    if "compliance_messages" not in st.session_state:
        st.session_state.compliance_messages = []
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None

def perform_similarity_search(prompt, k=5, score_threshold=0.5):
    if st.session_state.vectorstore is None:
        raise ValueError("Vector store is not initialized")
    
    retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": k})
    compressor = FlashrankRerank(model="ms-marco-MultiBERT-L-12")
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, 
        base_retriever=retriever
    )
    compressed_docs = compression_retriever.get_relevant_documents(prompt)
    filtered_results = [(doc, getattr(doc, 'score', 1.0)) for doc in compressed_docs]
    return filtered_results

# Query Expansion을 위한 프롬프트 템플릿
QUERY_EXPANSION_TEMPLATE = """
You are container shipping expert who can extract relevant data from given documentation. 
Given the following user query about shipping, extract the following information:
1. The Country of the Port of Loading (POL)
2. The Country of the Port of Discharging (POD)
3. Cargo Type

If any of these are not explicitly mentioned, use "Unknown" as the value.

User Query: {query}

Provide the extracted information in JSON format.
"""

query_expansion_prompt = PromptTemplate(
    input_variables=["query"],
    template=QUERY_EXPANSION_TEMPLATE
)

# Node 함수들
def expand_query(state):
    query = state['query']
    expansion_chain = query_expansion_prompt | llm | StrOutputParser()
    
    print(f"Original query: {query}")
    
    result = expansion_chain.invoke({"query": query})
    print(f"Raw result from expansion_chain: {result}")
    
    # 백틱과 'json' 문자열 제거
    result = result.replace("```json", "").replace("```", "").strip()
    
    try:
        expanded = json.loads(result)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON: {result}")
        expanded = {}
    
    print(f"Expanded result: {expanded}")
    
    state['expanded_query'] = {
        "original_query": query,
        "loading_country": expanded.get("Port of Loading Country", "Unknown"),
        "discharging_country": expanded.get("Port of Discharging Country", "Unknown"),
        "cargo_type": expanded.get("Cargo Type", "Unknown")
    }
    
    print(f"Final expanded query: {state['expanded_query']}")
    
    return state

def retrieve_loading_country(state):
    query = f"{state['expanded_query']['original_query']} {state['expanded_query']['loading_country']}"
    results = perform_similarity_search(query)
    state['retrieved_docs_loading'] = [doc for doc, _ in results]
    return state

def retrieve_discharging_country(state):
    query = f"{state['expanded_query']['original_query']} {state['expanded_query']['discharging_country']}"
    results = perform_similarity_search(query)
    state['retrieved_docs_discharging'] = [doc for doc, _ in results]
    return state

def retrieve_cargo_type(state):
    query = f"{state['expanded_query']['original_query']} {state['expanded_query']['cargo_type']}"
    results = perform_similarity_search(query)
    state['retrieved_docs_cargo'] = [doc for doc, _ in results]
    return state

def generate_response(docs, query):
    formatted_docs = "\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])
    return rag_chain.invoke({"formatted_documents": formatted_docs, "question": query})

def generate_responses(state):
    original_query = state['expanded_query']['original_query']
    state['generated_responses'] = [
        generate_response(state['retrieved_docs_loading'], original_query),
        generate_response(state['retrieved_docs_discharging'], original_query),
        generate_response(state['retrieved_docs_cargo'], original_query)
    ]
    return state

def fuse_results(state):
    generated_responses = state['generated_responses']
    fusion_prompt = PromptTemplate(
        input_variables=["results"],
        template="Given the following generated responses, create a comprehensive and coherent answer:\n\n{results}\n\nFused response:"
    )
    fusion_chain = fusion_prompt | llm | StrOutputParser()
    state['final_response'] = fusion_chain.invoke({"results": "\n\n".join(generated_responses)})
    return state

# LangGraph 구성
def create_rag_graph():
    workflow = StateGraph(GraphState)

    # Node 정의
    workflow.add_node("expand_query", expand_query)
    workflow.add_node("retrieve_loading", retrieve_loading_country)
    workflow.add_node("retrieve_discharging", retrieve_discharging_country)
    workflow.add_node("retrieve_cargo", retrieve_cargo_type)
    workflow.add_node("generate_responses", generate_responses)
    workflow.add_node("fuse_results", fuse_results)

    # Edge 정의
    workflow.add_edge("expand_query", "retrieve_loading")
    workflow.add_edge("expand_query", "retrieve_discharging")
    workflow.add_edge("expand_query", "retrieve_cargo")
    workflow.add_edge("retrieve_loading", "generate_responses")
    workflow.add_edge("retrieve_discharging", "generate_responses")
    workflow.add_edge("retrieve_cargo", "generate_responses")
    workflow.add_edge("generate_responses", "fuse_results")
    workflow.add_edge("fuse_results", END)

    # 병렬 처리를 위한 분기 설정
    workflow.set_entry_point("expand_query")
    
    return workflow.compile()

# GraphState 클래스 정의
class GraphState(dict):
    query: str
    expanded_query: Dict[str, str]
    retrieved_docs_loading: List[Document]
    retrieved_docs_discharging: List[Document]
    retrieved_docs_cargo: List[Document]
    generated_responses: List[str]
    final_response: str

def main():
    st.markdown(get_custom_font_css(), unsafe_allow_html=True)
    st.title("CHERRY Shipping Line Company Policy Search")
    
    initialize_vector_db()
    initialize_session_state()

    if st.session_state.vectorstore is None:
        st.error("Vector DB initialization failed. Please check your data and try again.")
        return

    # Display chat messages
    for message in st.session_state.compliance_messages:
        with st.chat_message(message["role"]):
            st.markdown(f"{message['content']}\n\n<div style='font-size:0.8em; color:#888;'>{message['timestamp']}</div>", unsafe_allow_html=True)
            if "steps" in message and message["role"] == "assistant":
                with st.expander("View documents"):
                    st.write(message["steps"])

    # Chat input
    user_input = st.chat_input("Any question about CHERRY Shipping Line Company Policy?")

    if user_input:
        # Add user message
        user_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.compliance_messages.append({"role": "user", "content": user_input, "timestamp": user_timestamp})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(f"{user_input}\n\n<div style='font-size:0.8em; color:#888;'>{user_timestamp}</div>", unsafe_allow_html=True)
        
        # Get AI response
        with st.spinner("Thinking..."):
            try:
                rag_graph = create_rag_graph()
                
                # 그래프 실행
                result = rag_graph.invoke({
                    "query": user_input,
                    "expanded_query": {},
                    "retrieved_docs_loading": [],
                    "retrieved_docs_discharging": [],
                    "retrieved_docs_cargo": [],
                    "generated_responses": [],
                    "final_response": ""
                })
                
                print(f"Final result from rag_graph: {result}")
                
                ai_response = result['final_response']
                ai_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
                # Add and display AI response
                st.session_state.compliance_messages.append({"role": "assistant", "content": ai_response, "timestamp": ai_timestamp})
                with st.chat_message("assistant"):
                    st.markdown(f"{ai_response}\n\n<div style='font-size:0.8em; color:#888;'>{ai_timestamp}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                print(f"Error details: {traceback.format_exc()}")
                return  # 오류 발생 시 함수 종료
        
        st.rerun()

if __name__ == "__main__":
    main()