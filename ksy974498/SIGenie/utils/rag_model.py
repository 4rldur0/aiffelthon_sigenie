import os
import streamlit as st
import datetime
import uuid
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.chat_models import ChatOpenAI  # If you're using OpenAI's ChatGPT API
from typing import List
from glob import glob

from openai import AsyncOpenAI

from utils.llms import get_llm
from utils.prompt.prompt_templates import rag_prompt_template

from dotenv import load_dotenv
load_dotenv()

# Step 1: Load documents from web or local sources (PDFs and URLs)
def load_documents(sources: List[str]) -> List:
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

# Step 2: Create the FAISS vector store
def create_vectorstore(documents):
    """
    Create and save the FAISS vector store for document retrieval.
    """
    embedding_model = OpenAIEmbeddings()
    
    # Use RecursiveCharacterTextSplitter to split long documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = text_splitter.split_documents(documents)
    
    # Create FAISS vectorstore from split documents and embeddings
    vectorstore = FAISS.from_documents(split_docs, embedding_model)
    
    # Save the FAISS vectorstore locally to disk
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
        # Load documents from the provided sources (URLs or PDFs)
        documents = load_documents(sources)
        return create_vectorstore(documents)

# Step 4: Build Retrieval-Augmented Generation Pipeline
class RAGModel:
    def __init__(self, rag_prompt_template, sources: List[str]):
        self.vectorstore = load_vectorstore(sources)
    
        # Setup the prompt template and chain
        self.prompt = PromptTemplate(template=rag_prompt_template, input_variables=["si_data"])
        self.llm = get_llm("gpt-4o-mini")
        self.chain = self.prompt | self.llm | StrOutputParser()

    def retrieve_documents(self, question: str):
        """
        Function to retrieve relevant documents from the vectorstore based on the question (SI data).
        """
        retriever = self.vectorstore.as_retriever(search_kwargs={'k': 5})  # Retrieve top 5 relevant documents
        relevant_docs = retriever.get_relevant_documents(question)
        return relevant_docs

    def generate_response(self, si_data: str, retrieved_docs: list):
        """
        Generate a response using the retrieved documents and the language model.
        """
        # Concatenate document contents to include in the prompt
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        question_with_context = f"{si_data}\n\nRelevant Documents:\n{context}"
        
        # Generate a response using the LLM chain
        return self.chain.astream({'si_data':question_with_context})

    def invoke(self, si_data: str):
        """
        Main function to retrieve documents and generate a response for compliance validation.
        """
        # Step 1: Retrieve relevant compliance documents
        retrieved_docs = self.retrieve_documents(si_data)
        
        # Step 2: Generate response based on SI data and retrieved documents
        response = self.generate_response(si_data, retrieved_docs)
        
        return response

# # Example usage
# if __name__ == "__main__":
# Define the list of URLs and local PDF files to load
urls = [
    "https://www.ilovesea.or.kr/dictionary/list.do",
]
pdf_files = glob('./docs/*.pdf')  # Adjust path to your PDF files
sources = pdf_files + urls

# Initialize the RAG model with sources
app = RAGModel(sources=sources, rag_prompt_template=rag_prompt_template)