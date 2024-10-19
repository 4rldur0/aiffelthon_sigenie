import os
from pymongo import MongoClient
from typing import List, Dict

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")
collection_name = 'si'
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "containergenie.ai"
os.environ['USER_AGENT'] = 'chapter2-1'

###################################################################################

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_tool_calling_agent, AgentExecutor

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

# time saver in the reference to the pdf file
def get_or_create_vector_store(pdf_path: str, vector_store_dir: str) -> FAISS:
    """
    Load existing vector store or create a new one if it doesn't exist
    """
    # 벡터 스토어 디렉토리가 존재하는지 확인
    if os.path.isdir(vector_store_dir) and \
       os.path.exists(os.path.join(vector_store_dir, "index.faiss")) and \
       os.path.exists(os.path.join(vector_store_dir, "index.pkl")):
        print(f"Loading existing vector store from {vector_store_dir}...")
        embeddings = OpenAIEmbeddings()
        return FAISS.load_local(vector_store_dir, embeddings, allow_dangerous_deserialization=True)
    
    print(f"Creating new vector store in {vector_store_dir}...")
    # 디렉토리가 없으면 생성
    os.makedirs(vector_store_dir, exist_ok=True)
    
    # PDF 로드 및 분할
    loader = PyMuPDFLoader(pdf_path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=50,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    documents = loader.load_and_split(text_splitter)
    
    # 벡터 스토어 생성 및 저장
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(documents=documents, embedding=embeddings)
    vector_store.save_local(vector_store_dir)
    
    return vector_store

def setup_pdf_retriever(pdf_path: str, vector_store_dir: str):
    """
    Setup PDF retriever tool using cached vector store
    """
    vector_store = get_or_create_vector_store(pdf_path, vector_store_dir)
    retriever = vector_store.as_retriever()
    
    return create_retriever_tool(
        retriever,
        name="pdf_search",
        description="Use this tool for compliance for shipper, consignee, and notifyParty" \
                    "including checking what info is required for each entity" \
                    "based on the requirements of both the company and relevant countries",
    )

# 사용 예시
PDF_PATH = "./CHERRY Shipping Line Company Policy.pdf"
VECTOR_STORE_DIR = "./chpt2.1_vector_store"  # 이것은 폴더 경로입니다

print("WARNING: This script loads a local vector store using pickle deserialization.")
print("Only run this if you trust the source of the vector store file.")

# 벡터 스토어 로드 또는 생성
pdf_retriever_tool = setup_pdf_retriever(PDF_PATH, VECTOR_STORE_DIR)

# 이후 코드는 동일하게 유지
tools = [pdf_retriever_tool]
#################################################################################

# llm & prompt
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
llm = ChatOpenAI(model='gpt-4o',temperature=0)

system_template = """
You are a documentation validation assistant specializing in verifying party details in shipping instructions.
Analyze the shipper, consignee, and notifyParty information in the provided JSON data, ensuring all essential details are present and correctly formatted.

Instructions:
1. Carefully examine each party's details, explaining your thought process for each step.
2. Verify the presence and format of mandatory items: name, address (including postal code), phone or fax number, and email address.
3. Verify that phone or fax numbers match the general contact format for the respective country, including area codes.
4. Ensure email addresses are in the correct format and domain names are appropriate.
5. Note that the notifyParty can be the same as the consignee; this is acceptable.
   
Response Format:
Provide a summarized validation report for the shipping instruction using the following structure:

This is the summarized validation report for shipping instruction.

1. Shipper
- Address: [Valid/Invalid] - [Comment on format and When postal code is missing it falls into Invalid]
   - Phone/Fax: [Valid/Invalid/Missing] - [Comment on format and area code]
   - Email: [Valid/Invalid/Missing] - [Comment on format]

2. Consignee
   - Address: [Valid/Invalid] - [Comment on format and When postal code is missing it falls into Invalid]
   - Phone/Fax: [Valid/Invalid/Missing] - [Comment on format and area code]
   - Email: [Valid/Invalid/Missing] - [Comment on format]

3. Notify Party
   - Address: [Valid/Invalid] - [Comment on format and When postal code is missing it falls into Invalid]
   - Phone/Fax: [Valid/Invalid/Missing] - [Comment on format and area code]
   - Email: [Valid/Invalid/Missing] - [Comment on format]
   
Overall Status: [All Valid/Invalid] - [Brief summary of issues if invalid, highlighting any missing postal codes]
"""

human_template = """
Data:
{data}

{agent_scratchpad}
"""

system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

# agent building
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# for result check
data = fetch_data_from_mongodb(collection_name, {"bookingReference": "CHERRY202411065640"})
# print(data[0]['bookingReference'])
# data[0]['partyDetails']

# execute agent
result = agent_executor.invoke({"bookingReference": data[0]['bookingReference'], "data": data[0]['partyDetails']})
print(result['output'])
