import os
import datetime
import logging
import random
import re
from typing import List
from langchain.schema import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import load_prompt
from langchain.text_splitter import RecursiveCharacterTextSplitter, TextSplitter
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv

# for reranker
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank

# Load environment variables
load_dotenv()

# Constants
PDF_PATH = "../docs/CHERRYShippingLineCompanyPolicy.pdf"
VECTOR_STORE_PATH = "../vector/compliance_faiss_index"
LAST_UPDATE_FILE = f"{VECTOR_STORE_PATH}/last_update.txt"

# Ensure necessary directories exist
os.makedirs(VECTOR_STORE_PATH, exist_ok=True)

# Set up OpenAI API
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings()


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

def update_faiss_index(PDF_PATH):
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


# def perform_similarity_search(vectorstore, prompt, k=5, score_threshold=0.5):
#     """
#     Perform similarity search on the vectorstore.
    
#     Args:
#     vectorstore: The FAISS vectorstore
#     prompt: The search query
#     k: Number of results to return
#     score_threshold: Threshold for filtering results based on similarity score
    
#     Returns:
#     List of tuples containing (document, score)
#     """
#     results = vectorstore.similarity_search_with_score(prompt, k=k)
    
#     # Filter results based on score threshold
#     filtered_results = [(doc, score) for doc, score in results if score <= score_threshold]
    
#     return filtered_results

# for reranker
def perform_similarity_search(vectorstore, prompt, k=10, score_threshold=0.5):
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