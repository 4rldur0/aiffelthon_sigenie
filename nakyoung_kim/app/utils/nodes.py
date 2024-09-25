import glob
from typing import TypedDict
from utils.prompt_templates import *
from utils.llms import get_llm
from utils.rag_model import RAGModel
from langchain.prompts import PromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.output_parsers.string import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = get_llm("gpt-4o-mini")

class State(TypedDict):
    parties_answer: str
    policy_answer: str
    news_answer: str
    summary_answer: str
    si_data: dict  # Changed from str to dict to reflect nested data structure in si_data
    next: str

def check_parties(state: State) -> State:
    prompt = PromptTemplate(template=check_parties_prompt, input_variables=["si_data"])
    chain = prompt | llm | StrOutputParser()
    try:
        response = chain.invoke({"si_data": state['si_data']})
        state['parties_answer'] = response
    except Exception as e:
        state['parties_answer'] = f"Error during checking parties: {e}"
    state['next'] = "validate_compliance"
    return state

def validate_compliance(state: State) -> State:
    """
    Function to validate shipping instruction data against compliance.
    Args:
        state (State): The state object containing si_data and other information.
    
    Returns:
        State: Updated state with compliance validation result.
    """
    urls = [
        "https://www.ilovesea.or.kr/dictionary/list.do",  # Replace with your URLs
    ]
    pdf_files = glob.glob('./docs/*.pdf')  # Adjust path to your PDF files
    sources = pdf_files + urls

    rag = RAGModel(llm=llm, sources=sources, template=validate_compliance_prompt)
    
    try:
        response = rag.invoke({"si_data": state['si_data']})
        state['policy_answer'] = response
    except Exception as e:
        state['policy_answer'] = f"Error during compliance validation: {e}"
    state['next'] = "search_news"
    return state

def search_news(state: State) -> State:
    web_search_tool = TavilySearchResults()

    try:
        query = f"News about {state['si_data']['routeDetails']['portOfLoading']} port and {state['si_data']['voyageDetails']['vesselName']} vessel"
        response = web_search_tool.invoke(query)
        state['news_answer'] = response
    except Exception as e:
        state['news_answer'] = f"Error during searching news: {e}"
    state['next'] = "generate_summary"
    return state

def generate_summary(state: State) -> State:
    prompt = PromptTemplate(template=summary_prompt, input_variables=["source"])
    chain = prompt | llm | StrOutputParser()
    try:
        response = chain.invoke(
            {"source": [state['parties_answer'], state['parties_answer']]}
        )
        state['summary_answer'] = response
    except Exception as e:
        state['summary_answer'] = f"Error generating summary: {e}"
    return state
