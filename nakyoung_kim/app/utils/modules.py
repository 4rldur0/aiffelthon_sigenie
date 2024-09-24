from utils.rag_model import RAGModel
from glob import glob
from utils.prompt_templates import *
from utils.llms import get_llm
from langchain.prompts import PromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.output_parsers.string import StrOutputParser
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = get_llm("gpt-4o-mini")

def check_missing(si_data):
    prompt = PromptTemplate(template=check_missing_prompt, input_variables=["si_data"]) # ChatPromptTemplate 써야햘까?
    chain =  prompt | llm | StrOutputParser()
    try:
        response = chain.invoke(si_data)
        return response
    except Exception as e:
        raise RuntimeError(f"Error during checking missing data: {e}")
    
async def check_parties(si_data):
    prompt = PromptTemplate(template=check_missing_prompt, input_variables=["si_data"]) # ChatPromptTemplate 써야햘까?
    chain =  prompt | llm | StrOutputParser()
    try:
        response = await chain.ainvoke(si_data)
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
    app = RAGModel(llm=llm, sources=sources, template=validate_compliance_prompt)
    question = f"Are there any compliance issues with the following shipping instruction: {si_data}?"
    
    try:
        # Directly await the final result from the invoke method
        response = await app.invoke(question)
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
    client = AsyncOpenAI()
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": summary_prompt},
                  {"role": "user", "content": source},],
        stream=True
    )
    streamed_text = ""
    for chunk in stream:
        chunk_content = chunk.choices[0].delta.content
        if chunk_content is not None:
            streamed_text = streamed_text + chunk_content
            placeholder.info(streamed_text)