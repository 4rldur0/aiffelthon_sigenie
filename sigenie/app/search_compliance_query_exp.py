import os
import streamlit as st
import datetime
import logging
import random
import re
import json
import logging
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

# 로깅 설정
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
    try:
        if 'vectorstore' not in st.session_state or st.session_state.vectorstore is None:
            if os.path.exists(os.path.join(VECTOR_STORE_PATH, "index.faiss")):
                try:
                    vectorstore = load_faiss_index()
                    logging.info("Existing Vector DB loaded.")
                    st.info("Existing Vector DB loaded.")
                except Exception as e:
                    logging.error(f"Failed to load existing Vector DB: {e}")
                    st.warning(f"Failed to load existing Vector DB: {e}. Creating a new one...")
                    vectorstore = update_faiss_index()
            else:
                logging.info("Vector DB not found. Creating a new one...")
                st.warning("Vector DB not found. Creating a new one...")
                vectorstore = update_faiss_index()
            
            st.session_state.vectorstore = vectorstore
        
        if check_pdf_update():
            logging.info("PDF has been updated. Updating Vector DB...")
            st.warning("PDF has been updated. Updating Vector DB...")
            st.session_state.vectorstore = update_faiss_index()
            st.success("Vector DB updated successfully!")
        
        return True
    except Exception as e:
        logging.error(f"Error in initialize_vector_db: {e}")
        st.error(f"An error occurred while initializing the vector database: {e}")
        return False

def initialize_session_state():
    if 'compliance_messages' not in st.session_state:
        st.session_state.compliance_messages = []
    if 'recommended_prompts' not in st.session_state:
        st.session_state.recommended_prompts = []
    if 'last_refresh_time' not in st.session_state:
        st.session_state.last_refresh_time = None

def generate_recommended_prompts(vectorstore):
    predefined_topics = [
        "Bill of Lading requirements",
        "Cargo restrictions and special handling",
        "Payment terms and credit policies",
        "Weight requirements and VGM",
        "Dangerous goods handling",
        "Reefer cargo procedures",
        "Out of Gauge (OOG) cargo handling",
        "Country-specific shipping regulations",
        "Environmental compliance measures",
        "Customer service standards",
        "Claims procedures",
        "Container specifications",
        "Customs clearance requirements",
        "Transit time guarantees",
        "Booking and documentation processes"
    ]
    
    questions = []
    random.shuffle(predefined_topics)
    for topic in predefined_topics:
        results = vectorstore.similarity_search(topic, k=1)
        if results:
            content = results[0].page_content
            questions.append(f"What are the key points in CHERRY Shipping Line's policy regarding {topic.lower()}?")
        
        if len(questions) == 3:
            break
    
    if len(questions) < 3:
        default_questions = [
            "What are the main safety regulations in the CHERRY Shipping Line Company Policy?",
            "Explain the cargo handling procedures according to the company policy",
            "What are the documentation requirements for international shipments?"
        ]
        questions.extend(default_questions[:(3-len(questions))])
    
    random.shuffle(questions)
    logging.info(f"Generated prompts: {questions}")
    return questions[:3]

def initialize_session_state():
    if 'compliance_messages' not in st.session_state:
        st.session_state.compliance_messages = []
    if 'recommended_prompts' not in st.session_state:
        st.session_state.recommended_prompts = []
    if 'last_refresh_time' not in st.session_state:
        st.session_state.last_refresh_time = None

def refresh_prompts():
    if 'vectorstore' in st.session_state and st.session_state.vectorstore is not None:
        new_prompts = generate_recommended_prompts(st.session_state.vectorstore)
        st.session_state.recommended_prompts = new_prompts
    else:
        st.session_state.recommended_prompts = [
            "What are the main safety regulations in the CHERRY Shipping Line Company Policy?",
            "Explain the cargo handling procedures according to the company policy",
            "What are the documentation requirements for international shipments?"
        ]
    st.session_state.last_refresh_time = datetime.datetime.now()
    logging.info(f"Prompts refreshed at {st.session_state.last_refresh_time}")
    logging.info(f"New prompts: {st.session_state.recommended_prompts}")

def perform_similarity_search(vectorstore, prompt, k=5, score_threshold=0.5):
    """
    Perform similarity search on the vectorstore with reranking.
    """
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
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
Given the following user query about shipping policies, extract the following information:
1. Port of Loading Country
2. Port of Discharging Country
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
    result = expansion_chain.invoke({"query": query})
    try:
        expanded = json.loads(result)
        state['expanded_query'] = {
            "original_query": query,
            "loading_country": expanded.get("Port of Loading Country", "Unknown"),
            "discharging_country": expanded.get("Port of Discharging Country", "Unknown"),
            "cargo_type": expanded.get("Cargo Type", "Unknown")
        }
    except json.JSONDecodeError:
        state['expanded_query'] = {
            "original_query": query,
            "loading_country": "Unknown",
            "discharging_country": "Unknown",
            "cargo_type": "Unknown"
        }
    return state

def retrieve_loading_country(state):
    query = f"{state['expanded_query']['original_query']} {state['expanded_query']['loading_country']}"
    results = perform_similarity_search(st.session_state.vectorstore, query)
    state['retrieved_docs_loading'] = [doc for doc, _ in results]
    return state

def retrieve_discharging_country(state):
    query = f"{state['expanded_query']['original_query']} {state['expanded_query']['discharging_country']}"
    results = perform_similarity_search(st.session_state.vectorstore, query)
    state['retrieved_docs_discharging'] = [doc for doc, _ in results]
    return state

def retrieve_cargo_type(state):
    query = f"{state['expanded_query']['original_query']} {state['expanded_query']['cargo_type']}"
    results = perform_similarity_search(st.session_state.vectorstore, query)
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
    
    initialize_session_state()
    
    # Vector DB 초기화
    if initialize_vector_db():
        # Vector DB 초기화 확인
        if 'vectorstore' not in st.session_state or st.session_state.vectorstore is None:
            st.error("Vector database initialization failed. Please check the logs and try again.")
            return  # 초기화 실패 시 여기서 함수 종료
    else:
        st.error("Failed to initialize vector database. Please check the logs and try again.")
        return

    # 여기서 recommended_prompts 생성
    if 'vectorstore' in st.session_state and st.session_state.vectorstore is not None:
        st.session_state.recommended_prompts = generate_recommended_prompts(st.session_state.vectorstore)

    
    initialize_session_state()

    # Display chat messages
    for message in st.session_state.compliance_messages:
        with st.chat_message(message["role"]):
            st.markdown(f"{message['content']}\n\n<div style='font-size:0.8em; color:#888;'>{message['timestamp']}</div>", unsafe_allow_html=True)
            if "steps" in message and message["role"] == "assistant":
                with st.expander("View documents"):
                    st.write(message["steps"])

    # Recommended prompts
    st.write("Recommended Prompts:")
    col1, col2, col3 = st.columns(3)

    # Recommended prompts
    st.write("Recommended Prompts:")
    col1, col2, col3 = st.columns(3)
    prompt = None
    with col1:
        if st.button(st.session_state.recommended_prompts[0]):
            prompt = st.session_state.recommended_prompts[0]
    with col2:
        if st.button(st.session_state.recommended_prompts[1]):
            prompt = st.session_state.recommended_prompts[1]
    with col3:
        if st.button(st.session_state.recommended_prompts[2]):
            prompt = st.session_state.recommended_prompts[2]

    # Refresh recommended prompts button
    if st.button("Refresh Recommended Prompts"):
        refresh_prompts()
        st.rerun()

    # Display last refresh time
    st.write(f"Last refreshed: {st.session_state.last_refresh_time}")

    # Chat input
    user_input = st.chat_input("Any question about CHERRY Shipping Line Company Policy?")
    
    # Use recommended prompt if clicked, otherwise use user input
    prompt = user_input if user_input else prompt

    if prompt:
        # Add user message
        user_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.compliance_messages.append({"role": "user", "content": prompt, "timestamp": user_timestamp})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(f"{prompt}\n\n<div style='font-size:0.8em; color:#888;'>{user_timestamp}</div>", unsafe_allow_html=True)
        
        # Get AI response
        with st.spinner("Thinking..."):
            try:
                rag_graph = create_rag_graph()
                
                # 그래프 실행
                result = rag_graph.invoke({
                    "query": prompt,
                    "expanded_query": {},
                    "retrieved_docs_loading": [],
                    "retrieved_docs_discharging": [],
                    "retrieved_docs_cargo": [],
                    "generated_responses": [],
                    "final_response": ""
                })
                
                ai_response = result['final_response']
                ai_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
                # Add and display AI response
                st.session_state.compliance_messages.append({"role": "assistant", "content": ai_response, "timestamp": ai_timestamp})
                with st.chat_message("assistant"):
                    st.markdown(f"{ai_response}\n\n<div style='font-size:0.8em; color:#888;'>{ai_timestamp}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        
        st.rerun()

if __name__ == "__main__":
    main()