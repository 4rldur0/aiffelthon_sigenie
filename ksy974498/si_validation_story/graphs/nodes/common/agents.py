import os
from .tools import *
from langchain.prompts import PromptTemplate
from typing import List
from langchain_core.output_parsers import StrOutputParser

class BasicChain:
    def __init__(self, llm, prompt, input_variables):
        # Initialize your LLM
        self.llm = llm
        
        # Setup the prompt template and chain
        self.prompt = PromptTemplate(template=prompt, input_variables=input_variables)
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def __call__(self):
        return self.chain

# Build Retrieval-Augmented Generation Pipeline
class RAGAgent:
    def __init__(self, sources: List[str], generate_response_chain):
        self.vectorstore = Faiss.load_vectorstore(sources)
        self.chain = generate_response_chain

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

    def __call__(self, si_data: str):
        """
        Main function to retrieve documents and generate a response for compliance validation.
        """
        # Step 1: Retrieve relevant compliance documents
        retrieved_docs = self.retrieve_documents(si_data)
        
        # Step 2: Generate response based on SI data and retrieved documents
        response = self.generate_response(si_data, retrieved_docs)
        return response