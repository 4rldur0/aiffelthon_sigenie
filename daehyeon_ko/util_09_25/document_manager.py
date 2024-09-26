# Import Libraries
from typing import List
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import logging

# Set up logging for error tracking
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

def load_documents(sources: List[str]) -> List:
    """
    Load documents from the provided sources (PDFs or URLs).
    Args:
        sources (List[str]): List of source paths or URLs.
    
    Returns:
        List: List of loaded documents.
    """
    docs = []
    for source in sources:
        try:
            if source.startswith('http'):
                loader = WebBaseLoader(source)
            elif source.endswith('.pdf'):
                loader = PyPDFLoader(source)
            else:
                continue
            docs.extend(loader.load())
        except Exception as e:
            logging.error(f"Error loading from {source}: {e}")
    return docs

def create_vectorstore(documents, index_path: str = "faiss_index"):
    """
    Create and save the FAISS vector store for document retrieval.
    Args:
        documents (List): List of documents to be stored in vector format.
        index_path (str): Directory path to save the vector store.
    
    Returns:
        FAISS: Initialized FAISS vector store.
    """
    try:
        embedding_model = OpenAIEmbeddings()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        split_docs = text_splitter.split_documents(documents)
        vectorstore = FAISS.from_documents(split_docs, embedding_model)
        vectorstore.save_local(index_path)
        return vectorstore
    except Exception as e:
        logging.error(f"Error creating vector store: {e}")
        raise RuntimeError(f"Failed to create vector store: {e}")

  def load_vectorstore(sources: List[str], index_path: str = "faiss_index"):
    """
    Load the vector store from disk if it exists. 
    If not, load documents and create a new vector store.
    Args:
        sources (List[str]): List of document sources (URLs or PDF paths).
        index_path (str): Path to store or load the vector index.
    
    Returns:
        FAISS: Loaded or newly created FAISS vector store.
    """
    try:
        if os.path.exists(f"{index_path}/index.faiss"):
            return FAISS.load_local(index_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
        else:
            documents = load_documents(sources)
            return create_vectorstore(documents, index_path)
    except Exception as e:
        logging.error(f"Error loading or creating vector store: {e}")
        raise RuntimeError(f"Failed to load or create vector store: {e}")
