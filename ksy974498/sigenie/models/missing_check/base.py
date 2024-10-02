from utils.llms import get_llm
from langchain_core.output_parsers.string import StrOutputParser
from langchain.prompts import PromptTemplate

from prompt import missing_check_prompt

llm = get_llm("gpt-4o-mini")

def check_missing(si_data, llm):
    """
    Function to check for missing data in the shipping instruction using an LLM prompt.
    """
    prompt = PromptTemplate(
        template=missing_check_prompt,
        input_variables=["si_data"]
    )
    
    # Combine prompt with the LLM and parser
    chain = prompt | llm | StrOutputParser()
    
    try:
        # Synchronously invoke the LLM to check for missing data
        response = chain.invoke({"si_data": si_data})
        return response
    except Exception as e:
        raise RuntimeError(f"Error during checking missing data: {e}")