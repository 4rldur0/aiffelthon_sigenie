import streamlit as st
from utils.llms import get_llm
from utils.prompt.prompt_templates import summary_prompt
from langchain_core.output_parsers.string import StrOutputParser
from langchain.prompts import PromptTemplate
import asyncio

# Initialize LLM (gpt-4o-mini)
llm = get_llm("gpt-4o-mini")

def check_missing(si_data):
    """
    Function to check for missing data in the shipping instruction using an LLM prompt.
    """
    prompt = PromptTemplate(
        template="""
                Are there any missing data with the following shipping instruction:
                Except for Additional Information is needed.
                Find from following data :\n{si_data}.
                Just say `OK` or `MISSING` per group.
                """,
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

def generate_response(si_data, missing_data_result):
    """
    Function to generate a response summary for the shipping instruction using the LLM.
    """
    report = """
            # Summarize the Shipping Instruction below.
            Check your summary contains the information about Missing Data and `Mandatory information required in Shipping Instructions`.

            ## Shipping Instruction:
            {si_data}

            ## Missing Data Check Result:
            {missing_data_result}
            """
    
    # Prepare the final summary report by combining the prompt and the template
    prompt = PromptTemplate(
        template=report, #summary_prompt,
        input_variables=['si_data', 'missing_data_result']
    )
    
    # Combine the prompt, LLM, and parser
    chain = prompt | llm | StrOutputParser()
    
    try:
        # Asynchronously invoke the LLM for streaming output
        response = chain.astream({'si_data': si_data, 'missing_data_result': missing_data_result})
        return response
    except Exception as e:
        raise RuntimeError(f"Error during generating response: {e}")


# Async wrapper for the response generation
async def generate_response_async(si_data, missing_data_result):
    """
    Async wrapper for generating the summary response asynchronously.
    """
    return generate_response(si_data, missing_data_result)


# Function to generate the full summary report
async def generate_full_summary(si_data):
    """
    Asynchronously handle the missing data check and summary generation,
    and display a combined summary report.
    """
    with st.spinner("Running checks..."):
        try:
            # Run check_missing synchronously to find missing data
            missing_data_result = check_missing(si_data)
            
            # Generate the full summary report asynchronously
            response = await generate_response_async(si_data, missing_data_result)
            placeholder = st.empty()

            # Stream the result chunk by chunk using async for
            streamed_text = ''
            async for chunk in response:
                if chunk is not None:
                    streamed_text += chunk
                    placeholder.info(streamed_text)

        except Exception as e:
            st.error(f"An error occurred while generating the summary: {e}")

# Streamlit page to display the validation check
def show_llm_summary_page():
    """
    Streamlit page function to display and handle the LLM summary report.
    """
    st.title("LLM Summary Report")

    # Check if 'si_data' is present in session state
    if "si_data" not in st.session_state:
        st.error("No Shipping Instruction data found. Please perform a search first.")
        return

    # Retrieve the SI data from session state
    si_data = st.session_state["si_data"]

    # Button to initiate the validation check
    if st.button("Run Validation Check"):
        # Run the asynchronous summary generation function
        asyncio.run(generate_full_summary(si_data))
        st.success("Summary completed!")
    else:
        st.warning("Please search for a Shipping Instruction first.")


from st_pages.search_page import show_search_page

# Example usage of Streamlit page
if __name__ == "__main__":
    show_llm_summary_page()