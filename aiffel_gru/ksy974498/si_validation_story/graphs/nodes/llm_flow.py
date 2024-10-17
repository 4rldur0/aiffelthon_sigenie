# llm_flow.py
import operator
from typing import Annotated, Sequence

from langgraph.graph import END, StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
# from langchain_core.pydantic_v1 import BaseModel
from pydantic import BaseModel

from langchain.prompts import PromptTemplate
from common.prompts import check_missing_prompt, intake_report_prompt
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from common.schemas import ShipmentStatus, ShipmentSummary

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

def get_si(state: MyAppState):
    mongodb = MongoDB(collection_name="si")
    si_data = mongodb.find_one_booking_reference(state.messages[-1].content)
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
    return {"messages": [response]}

workflow.add_node("get_si", get_si)
workflow.add_node("check_missing_data", check_missing)
workflow.add_node("generate_intake_report", generate_intake_report)

workflow.add_edge("get_si", "check_missing_data")
workflow.add_edge("check_missing_data", "generate_intake_report")
workflow.add_edge("generate_intake_report", END)

workflow.set_entry_point("get_si")

graph = workflow.compile()