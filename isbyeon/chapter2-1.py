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

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
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

# look for relevant parts in pdfs
PDF_loader = PyMuPDFLoader("./CHERRY Shipping Line Company Policy.pdf")

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
tools = [PDF_retriever_tool]

# llm & prompt
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

prompt = PromptTemplate.from_template(
"""You are a documentation validation assistant specializing in verifying party details in shipping instructions.
Make sure shipper, consignee, and nofifyParty in the data contain all the essential info as guided below:

# data:
{data}

# Instructions:
1. walk through each step carefully, explaining the thought process in detail.             
2. It is the rule that you have to mention address, phone or fax number, and email address, which are fundamentally mandatory items.              
3. Use PDF_retriever_tool to tell whether email address is not required.
4. Confirm address is in proper format of the respective country with explicit numeric postal code.
5. Do not attempt to infer or provide any missing elements such as a postal code in the address.
6. Verify if phone or FAX number definitely matches the general contacts format with area code.
7. Check whether email address is in proper format.
8. NotifyParty can be the same as consignee, the point that does't matter at all.
9. Any closing remarks at the bottom of the report are not preferred.
10. After reaching the final answer, review the solution once more to ensure it is correct.


# Respond in the example as below:
This is the summarized validation report for shipping instruction.
*{bookingReference}*

1. Shipper
- Address: The address part is valid containing a postal code(12345) for the related country.
- Phone: The phone number format is right with a conventional area code(99) for the related country included.
- Email: An email address is omitted, the item which is required.

2. Consignee
- Address: The address part is invalid as a postal code(99999) for the related country is not shown.
- Phone: A phone number is not detected.
- Email: The email address is in the correct format.

3. Notify Party
- Address: The address input is void.
- Phone: The phone number format is provided without a conventional area code(11) for the related country.
- Email: The email address is left empty, the item which is not mandatory.

# Answer:
{agent_scratchpad}""")

# agent building
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# for result check
data = fetch_data_from_mongodb(collection_name, {"bookingReference": "CHERRY202411065640"})
# print(data[0]['bookingReference'])
# data[0]['partyDetails']

# execute agent
result = agent_executor.invoke({"bookingReference": data[0]['bookingReference'], "data": data[0]['partyDetails']})
print(result['output'])
