# Import Libraries
from typing import List
from document_manager import load_vectorstore
from rag_templete import rag_prompt_templete
from openai_llm_config import llm
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging

# Set up logging for error tracking
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')


class RAGModel:
    def __init__(self, sources: List[str]):
        try:
            # Initialize or load the vector store from document sources
            self.vectorstore = load_vectorstore(sources)
        except Exception as e:
            logging.error(f"Error initializing vector store: {e}")
            raise RuntimeError(f"Could not initialize vector store: {e}")
        
        self.llm = llm
        self.rag_prompt_template = rag_prompt_template

        # Set up the prompt template and chain for response generation
        self.prompt = PromptTemplate(template=self.rag_prompt_template, input_variables=["si_data"])
        self.chain = self.prompt | llm | StrOutputParser()

    def retrieve_documents(self, question: str):
        """
        Retrieve relevant documents from the vector store based on the user's question.
        Args:
            question (str): User's query for document search.
        
        Returns:
            List: List of relevant documents.
        """
        try:
            retriever = self.vectorstore.as_retriever(search_kwargs={'k': 5})
            relevant_docs = retriever.get_relevant_documents(question)
            return relevant_docs
        except Exception as e:
            logging.error(f"Error retrieving documents: {e}")
            raise RuntimeError(f"Document retrieval failed: {e}")

    def generate_response(self, si_data: str, retrieved_docs: list):
        """
        Generate a response based on the retrieved documents and the input data.
        Args:
            si_data (str): Shipping instruction data or query.
            retrieved_docs (list): List of relevant documents.
        
        Returns:
            str: Generated response from the language model.
        """
        try:
            context = "\n\n".join([doc.page_content for doc in retrieved_docs])
            question_with_context = f"{si_data}\n\nRelevant Documents:\n{context}"
            return self.chain.astream({'si_data': question_with_context})
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            raise RuntimeError(f"Failed to generate response: {e}")

    def invoke(self, si_data: str):
        """
        Main method to retrieve documents and generate a response.
        Args:
            si_data (str): Input data for compliance validation.
        
        Returns:
            str: Generated response for the given input.
        """
        try:
            retrieved_docs = self.retrieve_documents(si_data)
            response = self.generate_response(si_data, retrieved_docs)
            return response
        except Exception as e:
            logging.error(f"Error during invocation: {e}")
            raise RuntimeError(f"Invocation error: {e}")
