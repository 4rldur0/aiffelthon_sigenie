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
        return self.collection.find_one({'bookingReference': booking_reference})
    
class Faiss:
    def retrieve_pdf(pdf_path):
        # look for relevant parts in pdfs
        PDF_loader = PyMuPDFLoader(pdf_path)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50, length_function=len, separators=["\n\n", "\n", " ", ""])
        PDF_split_docs = PDF_loader.load_and_split(text_splitter)

        embeddings = OpenAIEmbeddings()

        PDF_vector = FAISS.from_documents(documents=PDF_split_docs, embedding=embeddings)

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