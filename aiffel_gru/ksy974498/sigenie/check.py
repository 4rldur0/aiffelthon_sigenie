import streamlit as st
from ksy974498.sigenie.utils.validation_check.rag_pipeline import validate_compliance
from ksy974498.sigenie.utils.base.modules import check_missing, check_parties
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Async wrapper for compliance validation
async def validate_compliance_async(si_data):
    """
    Async wrapper for compliance validation using the validate_compliance function.
    """
    # Assuming validate_compliance returns an async generator, return the generator itself
    return validate_compliance(si_data)

# Combine check_missing and check_parties with compliance validation into a summary
async def generate_full_summary(si_data):
    """
    Asynchronously handle the missing data, parties check, and compliance validation,
    and display a combined summary report.
    """
    with st.spinner("Running checks..."):
        try:
            # Run check_missing synchronously
            missing_data_result = check_missing(si_data)

            # Run check_parties asynchronously
            parties_result = await check_parties(si_data)

            # Generate the compliance question
            compliance_question = f"Are there any compliance issues with the following shipping instruction: {si_data}?"
            compliance_report_generator = await validate_compliance_async(compliance_question)

            # Prepare the final summary report
            report = f"""
            ## Missing Data Check Result:
            {missing_data_result}

            ## Parties Check Result:
            {parties_result}

            ## Compliance Report:
            """
            placeholder = st.empty()

            # Handle streaming the compliance report asynchronously using async for
            streamed_text = report
            async for chunk in compliance_report_generator:
                if chunk is not None:
                    streamed_text = streamed_text + chunk
                    placeholder.info(streamed_text)

        except Exception as e:
            st.error(f"An error occurred while generating the summary: {e}")

# Streamlit page to display the validation check
def show_summary_page():

    st.title("Shipping Instruction Validation Check")

    # Check if 'si_data' is present in session state
    if "si_data" not in st.session_state:
        st.error("No Shipping Instruction data found. Please perform a search first.")
        return

    # Get the SI data from session state
    si_data = st.session_state["si_data"]

    # Display the Shipping Instruction data (optional, can be removed if not needed)
    #st.subheader("Shipping Instruction Data:")
    #st.write(si_data)

    # Button to initiate the validation check
    if st.button("Run Validation Check"):
        # Run the asynchronous summary generation function
        asyncio.run(generate_full_summary(si_data))
        st.success("Summary completed!")

from st_pages.search_page import show_search_page

# Example usage of Streamlit page
if __name__ == "__main__":
    show_search_page()
    show_summary_page()