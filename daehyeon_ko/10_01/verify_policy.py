# Step 0 : Import Libraries
import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict, Any
from langchain_core.output_parsers import StrOutputParser
import asyncio
from web_search import WebSearch # web_search module from other file "web_search.py"

# Step 1: Load documents from web or local sources (PDFs and URLs)
def load_documents(sources: List[str]) -> List:
    """
    Load documents from the provided sources (PDFs or URLs).
    """
    docs = []
    for source in sources:
        try:
            if source.startswith('http'):
                print(f"Loading documents from URL: {source}")
                loader = WebBaseLoader(source)
            elif source.endswith('.pdf'):
                print(f"Loading documents from PDF: {source}")
                loader = PyPDFLoader(source)
            else:
                print(f"Unsupported source type: {source}")
                continue
            docs.extend(loader.load())
        except Exception as e:
            print(f"Error loading from {source}: {e}")
    return docs

# Step 2: Create the FAISS vector store
def create_vectorstore(documents):
    """
    Create and save the FAISS vector store for document retrieval.
    """
    embedding_model = OpenAIEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = text_splitter.split_documents(documents)
    vectorstore = FAISS.from_documents(split_docs, embedding_model)
    vectorstore.save_local("faiss_index")
    print("Vector store created and saved locally at 'faiss_index'.")
    return vectorstore

# Step 3: Load existing vectorstore or create a new one
def load_vectorstore(sources: List[str]):
    """
    Load the vector store from disk if it exists.
    If not, load documents and create a new vector store.
    """
    if os.path.exists("faiss_index/index.faiss"):
        print("Loading existing vector store from 'faiss_index'.")
        return FAISS.load_local("faiss_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True)
    else:
        print("Vector store not found. Loading documents and creating a new vector store.")
        documents = load_documents(sources)
        return create_vectorstore(documents)

# Step 4: Web search for updated sanction lists
def perform_web_search(si_data: Dict[str, Any], include_urls: List[str], exclude_urls: List[str]) -> List[Dict[str, str]]:
    """
    Perform a web search to find updated sanction lists related to SI data.
    """
    search_results = []
    try:
        search_query = f"Find sanction list related to {si_data['SHIPPER']}, {si_data['CONSIGNEE']}, {si_data['NOTIFY']}, {si_data['HS_CODE']}, {si_data['CARGO_ITEM']}"
        search_engine = WebSearch()  # Initialize web search module
        search_results = search_engine.search(
            query=search_query, include_urls=include_urls, exclude_urls=exclude_urls
        )
    except Exception as e:
        print(f"Error performing web search: {e}")
    return search_results


# SI data validation function with web search
def validate_si_data(si_data: Dict[str, Any], compliance_docs: List[str], include_urls: List[str], exclude_urls: List[str]) -> List[str]:
    """
    Validate the SI data against CHERRY shipping line's company policy using both RAG and web search.
    """
    issues = []
    # Check with RAG (local compliance documents)
    sanctioned_keywords = ["sanctioned entity", "restricted item"]  # Example keywords
    for field in ['SHIPPER', 'CONSIGNEE', 'NOTIFY', 'HS_CODE', 'CARGO_ITEM']:
        if any(keyword in si_data.get(field, "").upper() for keyword in sanctioned_keywords):
            issues.append(f"{field} against the Sanctions of UN, EU or USA")

    # Check Description of Packages and Goods
    if "COMMERCIAL VALUE" in si_data.get('DESCRIPTION_OF_PACKAGES', "").upper():
        issues.append("Commercial value should not be included in cargo description.")
    
    # Check Embargo items at Port of Loading and Discharging
    embargo_items = ["restricted item", "embargoed goods"]  # Example keywords
    if any(item in si_data.get('DESCRIPTION_OF_PACKAGES', "").upper() for item in embargo_items):
        issues.append("Articles under the embargo at Port of Loading and Port of Discharging.")
    
    # Check Weight and Measurement notation
    if not validate_weight_and_measurement(si_data.get('CARGO_WEIGHT'), si_data.get('CARGO_MEASUREMENT')):
        issues.append("Cargo weight and measurement should be formatted to three decimal places.")
    
    # Check with web search (updated sanction lists)
    web_search_results = perform_web_search(si_data, include_urls, exclude_urls)
    if web_search_results:
        for result in web_search_results:
            if "sanction" in result['content'].lower():
                issues.append(f"Updated sanction found in web search: {result['title']} - {result['url']}")
    
    return issues

# Helper function for weight and measurement validation
def validate_weight_and_measurement(weight: str, measurement: str) -> bool:
    """
    Validate weight and measurement format to ensure three decimal places.
    """
    try:
        weight_valid = abs(float(weight) - round(float(weight), 3)) < 1e-9
        measurement_valid = abs(float(measurement) - round(float(measurement), 3)) < 1e-9
        return weight_valid and measurement_valid
    except (ValueError, TypeError):
        return False

# Step 5: Build Retrieval-Augmented Generation Pipeline
class RAGModel:
    def __init__(self, llm, sources: List[str], template, include_urls: List[str], exclude_urls: List[str]):
        self.vectorstore = load_vectorstore(sources)
        self.llm = llm
        self.prompt = PromptTemplate(template=template, input_variables=["si_data"])
        self.chain = self.prompt | self.llm | StrOutputParser()
        self.include_urls = include_urls
        self.exclude_urls = exclude_urls

    def retrieve_documents(self, question: str):
        """
        Retrieve relevant documents from the vectorstore based on the question (SI data).
        """
        retriever = self.vectorstore.as_retriever(search_kwargs={'k': 5})
        relevant_docs = retriever.get_relevant_documents(question)
        return relevant_docs

    def generate_response(self, si_data: str, retrieved_docs: list):
        """
        Generate a response using the retrieved documents and the language model.
        """
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        question_with_context = f"{si_data}\n\nRelevant Documents:\n{context}"
        return self.chain.invoke({'si_data': question_with_context})

    def validate_and_generate(self, si_data: Dict[str, Any]):
        """
        Validate SI data and generate response for compliance validation using RAG and web search.
        """
        # Step 5-1: Validate SI data against policy using both RAG and web search
        issues = validate_si_data(si_data, self.vectorstore, self.include_urls, self.exclude_urls)
        if issues:
            print("Found the following issues in SI data:")
            for issue in issues:
                print(f"- {issue}")
            return {"issues": issues}
        
        # Step 5-2: Retrieve relevant compliance documents
        retrieved_docs = self.retrieve_documents(si_data['DESCRIPTION_OF_PACKAGES'])
        
        # Step 5-3: Generate response based on SI data and retrieved documents
        response = self.generate_response(si_data['DESCRIPTION_OF_PACKAGES'], retrieved_docs)
        print(response)
        return response
