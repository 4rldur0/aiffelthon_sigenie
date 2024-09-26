from utils.rag_model import RAGModel
from glob import glob
from utils.prompt_templates import *
from utils.llms import get_llm
from langchain.prompts import PromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.output_parsers.string import StrOutputParser
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

# Initialize the language model
llm = get_llm("gpt-4o-mini")

# Function to check for missing data
def check_missing(si_data):
    prompt = PromptTemplate(template='Are there any Missing Data with the following shipping instruction: {si_data}', 
                            input_variables=["si_data"])
    chain = prompt | llm | StrOutputParser()
    try:
        response = chain.invoke({"si_data": si_data})
        return response
    except Exception as e:
        raise RuntimeError(f"Error during checking missing data: {e}")

# Asynchronous function to check parties
async def check_parties(si_data):
    prompt = PromptTemplate(template=check_parties_prompt, input_variables=["si_data"])
    chain = prompt | llm | StrOutputParser()
    try:
        response = await chain.ainvoke({"si_data": si_data})
        return response
    except Exception as e:
        raise RuntimeError(f"Error during checking parties: {e}")

# Function to combine results and generate a summary
async def generate_summary(si_data):
    """
    Generate a summary by combining results from check_missing and check_parties functions.
    """
    try:
        # Run check_missing and check_parties
        missing_data_result = check_missing(si_data)
        parties_result = await check_parties(si_data)
        
        # Construct the summary report
        report = f"""
        ## Missing Data Check Result:
        {missing_data_result}

        ## Parties Check Result:
        {parties_result}
        """

        # Prepare the summary prompt
        summary_template = PromptTemplate(template=summary_prompt, input_variables=["report"])
        summary_chain = summary_template | llm | StrOutputParser()

        # Generate the final summary using the LLM
        summary_response = summary_chain.astream({"report": report})
        return summary_response

    except Exception as e:
        raise RuntimeError(f"Error generating summary: {e}")


# async def generate_summary(placeholder, source: list):
#     """
#     Generate a summary using the retrieved 'check_parties_result' and 'search_news_result' data.
    
#     Parameters:
#     - placeholder: Streamlit placeholder to display results or errors.
#     - source: List containing 'check_parties_result' and 'search_news_result'.
#     """
#     # Unpack the source data
#     [check_parties_result, search_news_result] = source

#     client = AsyncOpenAI()  # Assuming AsyncOpenAI is set up to work with GPT models

#     # Construct the report for the summary
#     report = f"""
#     ## Check Parties Result
#     {check_parties_result}

#     ## Reference News
#     {search_news_result}
#     """
    
#     # Create the messages for the streaming LLM request
#     messages = [
#         {"role": "system", "content": summary_prompt},
#         {"role": "user", "content": report},
#     ]
    
#     try:
#         # Stream the response using the OpenAI API
#         stream = await client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=messages,
#             stream=True
#         )
        
#         # Handle the streamed response
#         streamed_text = ""
#         async for chunk in stream:
#             chunk_content = chunk.choices[0].delta.get("content", "")
#             if chunk_content:
#                 streamed_text += chunk_content
#                 placeholder.info(streamed_text)  # Update the Streamlit placeholder in real-time

#     except Exception as e:
#         placeholder.error(f"Error generating summary: {e}")