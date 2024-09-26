import streamlit as st
from glob import glob
from utils.prompt_templates import summary_prompt
from utils.llms import get_llm
from langchain.prompts import PromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.output_parsers.string import StrOutputParser
from dotenv import load_dotenv
from openai import AsyncOpenAI
import asyncio

load_dotenv()

llm = get_llm("gpt-4o-mini")

def generate_summary(placeholder, source):
    # Create a prompt template with the required input variables

    check_parties_result, search_news_result = source
    summary_template = PromptTemplate(template=summary_prompt)
    prompt = PromptTemplate(template="## check parties result\n{check_parties_result}\n\n## reference news\n{search_news_result}", 
                            input_variables=['check_parties_result', 'search_news_result'])
    combined = summary_template + prompt
    chain = combined | llm | StrOutputParser()
    try:
        # Get the result asynchronously
        response = chain.astream({"source": source})
        return response
    except Exception as e:
        placeholder.error(f"Error generating summary: {e}")

async def generate_summary_async(question: str):
    """
    Async wrapper for compliance validation to fit the async framework.
    """
    return generate_summary(question)

async def show_summary_report(si_data):

    question = f"Summarize the following shipping instruction: {si_data}?"

    # Use RAG pipeline to validate the fetched SI data for compliance asynchronously
    with st.spinner("Validating shipping instruction for compliance..."):
        try:
            # Fetch the compliance report asynchronously
            report = await generate_summary_async(question)
            placeholder = st.empty()

            if report:
                # Assuming the compliance report is a generator or an iterable, handle streaming the content
                streamed_text = ""
                async for chunk in report:
                    if chunk is not None:
                        streamed_text = streamed_text + chunk
                        placeholder.info(streamed_text)
            else:
                st.error("No relevant compliance information found.")
        except Exception as e:
            st.error(f"An error occurred during compliance verification: {e}")

