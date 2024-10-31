import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.tools.tavily_search import TavilySearchResults

# Load environment variables from .env file
load_dotenv()

class MongoDB:
    def __init__(self, collection_name: str):
        # Set up MongoDB connection using environment variables
        client = MongoClient(os.getenv("MONGODB_URI"))
        db = client[os.getenv("MONGODB_DB_NAME")]
        self.collection = db[collection_name]

    def find_one_booking_reference(self, booking_reference):
        return self.collection.find_one({'bookingReference': booking_reference}, {'_id': False })

from .vectorstore import *

class Faiss:
    def retrieve_pdf(pdf_path, vector_name):
        try:
            PDF_vector = FAISS.load_local(vector_name, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
        except:
            PDF_vector = update_faiss_index(pdf_path)
        
        PDF_retriever = PDF_vector.as_retriever()
        PDF_retriever_tool = create_retriever_tool(
            PDF_retriever,
            name="pdf_search",
            description="Use this tool for compliance for shipper, consignee, and notifyParty" \
                        "including checking what info is required for each entity" \
                        "based on the requirements of both the company and relevant countries",
        )
        
        return PDF_retriever_tool

    
class Tavily:
    def web_search():
        return TavilySearchResults()