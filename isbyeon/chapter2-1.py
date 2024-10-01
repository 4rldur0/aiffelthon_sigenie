MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")
collection_name = 'si'
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "containergenie.ai"
os.environ['USER_AGENT'] = 'chapter2-1'

####################################################################################
import os
from pymongo import MongoClient
from typing import List, Dict
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
###################################################################################

# block included to check whether the whole chain works out or not
def fetch_data_from_mongodb(collection_name: str, query: Dict = None, limit: int = None) -> List[Dict]:
 
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[collection_name]
    
    # Prepare the find operation
    find_operation = collection.find(query) if query else collection.find()
    
    # Fetch and return the data
    data = list(find_operation)
    
    # Close the connection
    client.close()
    
    return data


###################################################################################
# Build a set of tools 

## Search online results as many as 5
search = TavilySearchResults(k=5)


## look for relevant parts in pdfs

PDF_loader = PyPDFLoader("./cherry_compliance.pdf")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
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

## retrieve relevant info online
WebBase_loader = WebBaseLoader("https://www.ilovesea.or.kr/dictionary/list.do")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
WebBase_split_docs = WebBase_loader.load_and_split(text_splitter)

embeddings = OpenAIEmbeddings()

WebBase_vector = FAISS.from_documents(documents=WebBase_split_docs, embedding=embeddings)

WebBase_retriever = WebBase_vector.as_retriever()

WebBase_retriever_tool = create_retriever_tool(
    WebBase_retriever,
    name="web_search",
    description="Put this tool to use in a bid to check spelling of industry terminology",
)

# set of tools
tools = [search, PDF_retriever_tool, WebBase_retriever_tool]

###################################################################################

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = PromptTemplate.from_template(
    """You are an assistant to check whether there are few problems, if any.
    On the basis of {data}, make sure PartyDetails inclusive of shipper, consignee, and nofifyParty
    have to contain all the essential info the right way.
1. confirm address including zip code is in proper format of the respective country.
2. verify if phone or FAX number matches the general contacts format.     
3. notifyParty can be the same as consignee.

# Please respond in the following format:
This is the summarized validation report for shipping instruction\n
{query['bookingReference']}

1. Shipper
- detailed issue, if any

2. Consignee
- detailed issue, if any

3. Notify Party
- detailed issue, if any

# Answer:
"""
)


agent = create_openai_functions_agent(llm, tools, prompt)


agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)



data = fetch_data_from_mongodb(collection_name, {"bookingReference": "CHERRY202409072244"})
    

result = agent_executor.invoke({'bookingReference':"CHERRY202409072244",'data':data})
