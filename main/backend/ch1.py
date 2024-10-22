# ch1.py
from langgraph.graph import END, StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

from common import *
from fastapi import FastAPI

from dotenv import load_dotenv

load_dotenv()

workflow = StateGraph(MyAppState)
model = gpt_4o_mini

from common.tools import MongoDB

def get_bkg(state: MyAppState):
    mongodb = MongoDB(collection_name="bkg")
    si_data = mongodb.find_one_booking_reference(state.messages[-1].content)
    return {"messages": [HumanMessage(content=str(si_data))]}

def get_si(state: MyAppState):
    mongodb = MongoDB(collection_name="si")
    si_data = mongodb.find_one_booking_reference(state.messages[-2].content)
    return {"messages": [HumanMessage(content=str(si_data))]}


def check_missing(state: MyAppState):
    output_parser = JsonOutputParser(pydantic_object=ShipmentStatus)
    llm = model
    prompt = PromptTemplate(
            template=check_missing_prompt,
            input_variables=["si_data"],
            partial_variables={
                "format_instructions": output_parser.get_format_instructions()
            },
        )
    chain = prompt | llm | output_parser

    response = chain.invoke({'si_data': state.messages[-1]})

    # response를 HumanMessage로 변환하여 반환
    if isinstance(response, dict):
        response_message = HumanMessage(content=str(response))
    else:
        response_message = HumanMessage(content="Invalid response format.")
    return {"messages": [response_message]}

def generate_intake_report(state: MyAppState):
    output_parser = JsonOutputParser(pydantic_object=ShipmentSummary)
    llm = model
    prompt = PromptTemplate(
            template=intake_report_prompt,
            input_variables=["si_data",'missing_info'],
            partial_variables={
                "format_instructions": output_parser.get_format_instructions()
            },
        )
    chain = prompt | llm | output_parser
    response = chain.invoke({'si_data': state.messages[-2], 
                             'missing_info':state.messages[-1]})
    response_message = HumanMessage(content=str(response))
    return {"messages": [response_message]}

workflow.add_node("get_bkg", get_bkg)
workflow.add_node("get_si", get_si)
workflow.add_node("check_missing_data", check_missing)
workflow.add_node("generate_intake_report", generate_intake_report)

workflow.set_entry_point("get_bkg")
workflow.add_edge("get_bkg", "get_si")
workflow.add_edge("get_si", "check_missing_data")
workflow.add_edge("check_missing_data", "generate_intake_report")
workflow.add_edge("generate_intake_report", END)

graph = workflow.compile()