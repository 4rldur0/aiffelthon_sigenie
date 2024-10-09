import os
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import List

# Load environment variables from .env file
load_dotenv()

class MongoDB:
    def __init__(self, collection_name: str):
        # Set up MongoDB connection using environment variables
        client = MongoClient(os.getenv("MONGODB_URI"))
        db = client[os.getenv("MONGODB_DB_NAME")]
        self.collection = db[collection_name]

    def find_one_booking_reference(self, booking_reference):
        return self.collection.find_one({'bookingReference': booking_reference})
    
class Faiss:
    def __init__(self):
        self.save_local_path = "faiss_index"
        self.embedding_model = OpenAIEmbeddings()

    # Load documents from web or local sources (PDFs and URLs)
    def _load_documents(self, sources: List[str]) -> List:
        """
        Load documents from the provided sources (PDFs or URLs).
        """
        docs = []
        for source in sources:
            try:
                # If source is a URL
                if source.startswith('http'):
                    print(f"Loading documents from URL: {source}")
                    loader = WebBaseLoader(source)
                # If source is a PDF
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
    
    # Create the FAISS vector store
    def _create_vectorstore(self, documents):
        """
        Create and save the FAISS vector store for document retrieval.
        """        
        # Use RecursiveCharacterTextSplitter to split long documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        split_docs = text_splitter.split_documents(documents)
        
        # Create FAISS vectorstore from split documents and embeddings
        vectorstore = FAISS.from_documents(split_docs, self.embedding_model)
        
        # Save the FAISS vectorstore locally to disk
        vectorstore.save_local(self.save_local_path)
        print("Vector store created and saved locally at 'faiss_index'.")
        return vectorstore
    
    # Step 3: Load existing vectorstore or create a new one
    def load_vectorstore(self, sources: List[str]):
        """
        Load the vector store from disk if it exists.
        If not, load documents and create a new vector store.
        """
        if os.path.exists("faiss_index/index.faiss"):
            print("Loading existing vector store from 'faiss_index'.")
            return FAISS.load_local(self.save_local_path, self.embedding_model, allow_dangerous_deserialization=True)
        else:
            print("Vector store not found. Loading documents and creating a new vector store.")
            # Load documents from the provided sources (URLs or PDFs)
            documents = self._load_documents(sources)
            return self._create_vectorstore(documents)
        
class TavilySearch:
    def __call__():
        return TavilySearchResults()