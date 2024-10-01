import os
import json
from bson import json_util
from typing import List, Dict, TypedDict, Annotated, Sequence, Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pymongo import MongoClient
from operator import add
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")
collection_name = 'si'
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "containergenie.ai"

llm = ChatOpenAI(model='gpt-4o-mini',temperature=0.0)

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


def check_missing(data):
    prompt = PromptTemplate(
        template="Are there any missing data with the following collection: {data}?",
        input_variables=["data"]
    )
    llm = ChatOpenAI()  # You might want to customize this
    chain = prompt | llm | StrOutputParser()
    try:
        response = chain.invoke({"data": json_util.dumps(data)})
        return response
    except Exception as e:
        raise RuntimeError(f"Error during checking missing data: {e}")

def summarize_data(data, missing_info):
    prompt = PromptTemplate(
        template="Summarize the main information and missing data from this collection:\n\nData: {data}\n\nMissing Information: {missing_info}",
        input_variables=["data", "missing_info"]
    )
    chain = prompt | llm | StrOutputParser()
    try:
        response = chain.invoke({"data": json_util.dumps(data), "missing_info": missing_info})
        return response
    except Exception as e:
        raise RuntimeError(f"Error during summarizing data: {e}")
    
    # Define the state that will be passed between nodes
class GraphState(TypedDict):
    messages: Annotated[Sequence[HumanMessage | AIMessage], add]
    data: Optional[dict]
    missing_info: Optional[str]
    summary: Optional[str]
    booking_reference: str

# Node to fetch data from MongoDB
def fetch_data_node(state):
    booking_reference = state['booking_reference']
    data = fetch_data_from_mongodb(collection_name, {"bookingReference": booking_reference})
    return {"data": data}

# Node to check for missing data
def check_missing_node(state):
    data = state['data']
    missing_info = check_missing(json_util.dumps(data))
    return {"missing_info": missing_info}

# Node to summarize data and missing info
def create_summary_node(state):
    data = state['data']
    missing_info = state['missing_info']
    summary = summarize_data(json_util.dumps(data), missing_info)
    return {"summary": summary}

# Create the graph
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("fetch_data", fetch_data_node)
workflow.add_node("check_missing", check_missing_node)
workflow.add_node("create_summary", create_summary_node)

# Add edges
workflow.add_edge(START, 'fetch_data')
workflow.add_edge('fetch_data', 'check_missing')
workflow.add_edge('check_missing', 'create_summary')
workflow.add_edge('create_summary', END)

# Compile the graph
graph = workflow.compile()

# # 실행 함수
# def process_booking_reference(booking_reference: str):
#     inputs = {"booking_reference": booking_reference}
#     result = graph.invoke(inputs)
#     return result

# # 사용 예시
# if __name__ == "__main__":
#     booking_reference = "EXAMPLE123"
#     result = process_booking_reference(booking_reference)
#     print(f"Summary for booking reference {booking_reference}:")
#     print(result['summary'])


graph.invoke({"booking_reference": "CHERRY202409072244"})


from IPython.display import Image, display

try:
    display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass
