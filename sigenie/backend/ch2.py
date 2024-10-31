# ch2.py
from langgraph.graph import END, StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser


from langchain.prompts import PromptTemplate

from common import *
import os
from tavily import TavilyClient
# from ast import literal_eval
# import json

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

workflow = StateGraph(MyAppState)
model = gpt_4o_mini

def get_si(state: MyAppState):
    mongodb = MongoDB(collection_name="si")
    si_data = mongodb.find_one_booking_reference(state.messages[-1].content)
    return {"messages": [HumanMessage(content=str(si_data))]}

def check_parties(state: MyAppState):
    llm = model
    prompt = check_parties_prompt
    pdf_path = "./docs/CHERRYShippingLineCompanyPolicy.pdf"#os.path.join(os.path.abspath('docs'), "CHERRYShippingLineCompanyPolicy.pdf")
    rag = RAGAgent(prompt=prompt, llm=llm, pdf_path=pdf_path, vector_name='./vector/compliance_faiss_index')
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
    pdf_path = "./docs/CHERRYShippingLineCompanyPolicy.pdf"#os.path.join(os.path.abspath('docs'), "CHERRYShippingLineCompanyPolicy.pdf")
    rag = RAGAgent(prompt=prompt, llm=llm, pdf_path=pdf_path, vector_name='./vector/compliance_faiss_index')
    response = rag.invoke({'si_data': state.messages[-1]})

    # response를 HumanMessage로 변환하여 반환
    if isinstance(response, dict):
        response_message = HumanMessage(content=str(response['output']))
    else:
        response_message = HumanMessage(content="Invalid response format.")
    return {"messages": [response_message]}


def verify_vessel_port_situation(state: MyAppState):
    si_data = state.messages[-3].content
    llm = model

    prompt = PromptTemplate(
            template=query_prompt,
            input_variables=["si_data"],
        )
    
    chain = prompt | llm | StrOutputParser()
    search_query = chain.invoke(si_data)

    # 웹 검색 쿼리 작성
    client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
    response = client.search(search_query, include_answer=True)
    response = {'query' : response['query'],
                'answer': response['answer'],
                'results' : response['results']}
    response_message = HumanMessage(content=str(response))
    return {"messages": [response_message]}

def generate_validation_report(state: MyAppState):
    llm = model
    prompt = validation_report_prompt
    chain = BasicChain(llm, prompt, input_variables=["si_data", 'parties_check','verify_company_policy'])
    response = chain.invoke({"si_data": state.messages[-3].content, 
                             'parties_check' : state.messages[-2].content,
                             'verify_company_policy': state.messages[-1].content})
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