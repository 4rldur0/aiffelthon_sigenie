from utils.rag_model import RAGModel
from glob import glob
from utils.prompt_templates import *
from utils.llms import get_llm
from langchain.prompts import PromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.output_parsers.string import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = get_llm("gpt-4o-mini")

def check_missing(si_data):
    prompt = PromptTemplate(template=check_missing_prompt, input_variables=["si_data"])
    chain =  prompt | llm | StrOutputParser()
    try:
        response = chain.invoke({"si_data": si_data})
        return response
    except Exception as e:
        raise RuntimeError(f"Error during checking missing data: {e}")
    
async def check_parties(si_data):
    prompt = PromptTemplate(template=check_parties_prompt, input_variables=["si_data"])
    chain =  prompt | llm | StrOutputParser()
    try:
        response = await chain.ainvoke({"si_data": si_data})
        return response
    except Exception as e:
        raise RuntimeError(f"Error during checking parties: {e}")

async def validate_compliance(si_data):
    """
    Function to validate shipping instruction data against compliance.
    Args:
        si_data (str): The question or query to check for compliance.
    
    Returns:
        str: Generated compliance report or validation result.
    """
    # Define the list of URLs and local PDF files to load
    urls = [
        "https://www.ilovesea.or.kr/dictionary/list.do",  # Replace with your URLs
    ]
    pdf_files = glob('./docs/*.pdf')  # Adjust path to your PDF files
    sources = pdf_files + urls

    # Initialize the RAG model with sources
    rag = RAGModel(llm=llm, sources=sources, template=validate_compliance_prompt)
    question = f"Are there any compliance issues with the following shipping instruction: {si_data}?"
    
    try:
        # Directly await the final result from the invoke method
        response = await rag.invoke(question)
        return response
    except Exception as e:
        raise RuntimeError(f"Error during compliance validation: {e}")

async def search_news(si_data):
    web_search_tool = TavilySearchResults()

    query = f"search news about {si_data['routeDetails']['portOfLoading']} port and {si_data['voyageDetails']['vesselName']} vessel"
    try:
        response = await web_search_tool.ainvoke(query)
        return response
    except Exception as e:
        raise RuntimeError(f"Error during searching news: {e}")
    
def generate_summary(placeholder, source):
    prompt = PromptTemplate(template=summary_prompt, input_variables=["source"])
    chain = prompt | llm | StrOutputParser()
    try:
        # Get the result asynchronously
        response = chain.invoke({"source": source})
        placeholder.info(response)  # Display the result in the placeholder
    except Exception as e:
        placeholder.error(f"Error generating summary: {e}")