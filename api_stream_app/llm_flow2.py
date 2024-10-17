# llm_flow.py
import operator
from typing import Annotated, Sequence

from langgraph.graph import END, StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage

from pydantic import BaseModel

from langchain.prompts import PromptTemplate
from common.prompts import check_parties_prompt, verify_company_policy_prompt, validation_report_prompt


from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from common.schemas import ShipmentStatus, ShipmentSummary

from fastapi import FastAPI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from dotenv import load_dotenv

load_dotenv()

class MyAppState(BaseModel):
    messages: Annotated[Sequence[BaseMessage], operator.add]

workflow = StateGraph(MyAppState)
model = ChatOpenAI(temperature=0, 
                    model_name="gpt-4o-mini",
                    streaming=True,              
                    callbacks=[StreamingStdOutCallbackHandler()]
                    )

from common.tools import MongoDB
from common.agents import RAGAgent, BasicChain
import os

def get_si(state: MyAppState):
    mongodb = MongoDB(collection_name="si")
    si_data = mongodb.find_one_booking_reference(state.messages[-1].content)
    return {"messages": [HumanMessage(content=str(si_data))]}

def check_parties(state: MyAppState):
    llm = model
    prompt = check_parties_prompt
    pdf_path = os.path.join(os.path.abspath('docs'), "CHERRYShippingLineCompanyPolicy.pdf")
    rag = RAGAgent(prompt=prompt, llm=llm, pdf_path=pdf_path)
    response = rag.invoke({'si_data': state.messages[-1]})

    # response를 HumanMessage로 변환하여 반환
    if isinstance(response, dict):
        response_message = HumanMessage(content=str(response['output']))
    else:
        response_message = HumanMessage(content="Invalid response format.")
    return {"messages": [response_message]}

def verify_company_policy(state: MyAppState):
    llm = model
    prompt = verify_company_policy_prompt
    pdf_path = os.path.join(os.path.abspath('docs'), "CHERRYShippingLineCompanyPolicy.pdf")
    rag = RAGAgent(prompt=prompt, llm=llm, pdf_path=pdf_path)
    response = rag.invoke({'si_data': state.messages[-1]})

    # response를 HumanMessage로 변환하여 반환
    if isinstance(response, dict):
        response_message = HumanMessage(content=str(response['output']))
    else:
        response_message = HumanMessage(content="Invalid response format.")
    return {"messages": [response_message]}

import os
from tavily import TavilyClient
from ast import literal_eval
import json

def verify_vessel_port_situation(state: MyAppState):
    si_data = state.messages[-3].content
    llm = ChatOpenAI(temperature=0, 
                    model_name="gpt-4o-mini",
                    streaming=True,              
                    callbacks=[StreamingStdOutCallbackHandler()]
                    )
    query_prompt = """
    Based on the following shipment data, generate a concise web search query to find recent news about the port and vessel. 
    The search query should include the port of loading and the vessel name.

    Shipment Data:
    {si_data}

    Generate a search query that might return recent news about the status of the port and the vessel's voyage.
    """
    prompt = PromptTemplate(
            template=query_prompt,
            input_variables=["si_data"],
        )
    
    chain = prompt | llm | StrOutputParser()
    search_query = chain.invoke(si_data)

    # 웹 검색 쿼리 작성
    client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
    response = client.search(search_query, include_answer=True)
    response_message = HumanMessage(content=str(response))
    return {"messages": [response_message]}

def generate_validation_report(state: MyAppState):
    llm = model
    prompt = validation_report_prompt
    chain = BasicChain(llm, prompt, input_variables=["sources"])
    response = chain.invoke(
                {"sources": [state.messages[-3].content, state.messages[-2].content, state.messages[-1].content]}
            )
    response_message = HumanMessage(content=str(response))
    return {"messages": [response_message]}

# Add nodes
workflow.add_node("get_si", get_si)
workflow.add_node("check_parties", check_parties)
workflow.add_node("verify_company_policy", verify_company_policy)
workflow.add_node("verify_vessel_port_situation", verify_vessel_port_situation)
workflow.add_node("generate_validation_report", generate_validation_report)

# Add edges
workflow.set_entry_point("get_si")
workflow.add_edge("get_si", "check_parties")
workflow.add_edge("check_parties", "verify_company_policy")
workflow.add_edge("verify_company_policy", "verify_vessel_port_situation")
workflow.add_edge("verify_vessel_port_situation", "generate_validation_report")
workflow.add_edge("generate_validation_report", END)

graph = workflow.compile()