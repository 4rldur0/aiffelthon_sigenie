import os
from pymongo import MongoClient
from typing import List, Dict

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")
collection_name = 'si'
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "containergenie.ai"
os.environ['USER_AGENT'] = 'chapter2-1'

####################################################################################

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_openai_functions_agent, AgentExecutor

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
# Build a set of tools 

## Search online results as many as 5
search_tool = TavilySearchResults(k=5)

## look for relevant parts in pdfs

PDF_loader = PyPDFLoader("./CHERRY Shipping Line Company Policy.pdf")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50, length_function=len, separators=["\n\n", "\n", " ", ""])
PDF_split_docs = PDF_loader.load_and_split(text_splitter)
len(PDF_split_docs)

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
# set of tools
tools = [search_tool, PDF_retriever_tool]
# 1. Explain your reasoning process step by step.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

prompt = PromptTemplate.from_template(
"""You are a documentation validation assistant specializing in verifying party details in shipping instructions.
Make sure shipper, consignee, and nofifyParty in the {data} contain all the essential info as guided below:
              
1. Take a Chain of Thought approach in the process.
2. It is the rule that you have to mention address, phone or fax number, and email address, which are fundamentally mandatory items.              
3. Use PDF_retriever_tool to tell whether email address is not required.
4. Confirm address is in proper format of the respective country with explicit postal code like "07528" as in "SEOUL 07528, KOREA".
5. Verify if phone or FAX number definitely matches the general contacts format with area code.
6. Check whether email address is in proper format.
7. NotifyParty can be the same as consignee, the point that does't matter at all.
8. Don't improvise anything you don't know at all based on the given conditions.
9. Any wrap-up remarks at the bottom of the report are not preferred.

# Respond in the example as below:
This is the summarized validation report for shipping instruction.
*{bookingReference}*

1. Shipper
- Address: The address part is valid including a postal code for the related country. 
- Phone: The phone number format is right with a conventional area code for the related country included.
- Email: An email address is omitted, the item which is required.

2. Consignee
- Address: The address part is with some typos.  
- Phone: A phone number format is not found.
- Email: The email address is in the correct format.

3. Notify Party
- Address: The address input is void.  
- Phone: The phone number format is provided without a conventional area code for the related country.
- Email: The email address is left empty, the item which is required.

# Answer:
{agent_scratchpad}""")

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
data = fetch_data_from_mongodb(collection_name, {"bookingReference": "CHERRY202411139973"})
data
result = agent_executor.invoke({"bookingReference": "CHERRY202411139973", "data": data})
print(result['output'])
