import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.output_parsers import StrOutputParser
import asyncio

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
    def __init__(self, llm, sources: List[str], template: str):
        self.vectorstore = load_vectorstore(sources)
        
        # Initialize your LLM
        self.llm = llm
        
        # Setup the prompt template and chain
        self.prompt = PromptTemplate(template=template, input_variables=["si_data"])
        self.chain = self.prompt | self.llm | StrOutputParser()

    def retrieve_documents(self, query: str):
        """
        Function to retrieve relevant documents from the vectorstore based on the question (SI data).
        """
        retriever = self.vectorstore.as_retriever(search_kwargs={'k': 5})  # Retrieve top 5 relevant documents
        relevant_docs = retriever.invoke(str(query))
        return relevant_docs

    def generate_response(self, query: str, retrieved_docs: list):
        """
        Generate a response using the retrieved documents and the language model.
        """
        # Concatenate document contents to include in the prompt
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        
        # Generate a response using the LLM chain
        return self.chain.invoke({'query':query, 'context': context})

    def invoke(self, si_data: str):
        """
        Main function to retrieve documents and generate a response for compliance validation.
        """
        # Step 1: Retrieve relevant compliance documents
        retrieved_docs = self.retrieve_documents(si_data)
        
        # Step 2: Generate response based on SI data and retrieved documents
        response = self.generate_response(si_data, retrieved_docs)
        return response
    
class async_RAGModel:
    def __init__(self, llm, sources: List[str], template: str):
        self.vectorstore = load_vectorstore(sources)
        
        # Initialize your LLM
        self.llm = llm
        
        # Setup the prompt template and chain
        self.prompt = PromptTemplate(template=template, input_variables=["si_data"])
        self.chain = self.prompt | self.llm | StrOutputParser()

    async def retrieve_documents(self, query: str):
        """
        Async function to retrieve relevant documents from the vectorstore based on the question (SI data).
        """
        retriever = self.vectorstore.as_retriever(search_kwargs={'k': 5})  # Retrieve top 5 relevant documents
        relevant_docs = await asyncio.to_thread(retriever.invoke, str(query))  # Offload to thread
        return relevant_docs

    async def generate_response(self, query: str, retrieved_docs: list):
        """
        Async function to generate a response using the retrieved documents and the language model.
        """
        # Concatenate document contents to include in the prompt
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        
        # Generate a response using the LLM chain
        response = await asyncio.to_thread(self.chain.invoke, {'query': query, 'context': context})  # Offload to thread
        return response

    async def ainvoke(self, si_data: str):
        """
        Async main function to retrieve documents and generate a response for compliance validation.
        """
        # Step 1: Retrieve relevant compliance documents asynchronously
        retrieved_docs = await self.retrieve_documents(si_data)
        
        # Step 2: Generate response based on SI data and retrieved documents
        response = await self.generate_response(si_data, retrieved_docs)
        return response
