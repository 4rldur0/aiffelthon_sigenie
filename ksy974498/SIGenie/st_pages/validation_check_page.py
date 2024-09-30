import streamlit as st
from ksy974498.sigenie.utils.validation_check.rag_pipeline import validate_compliance
import asyncio

async def validate_compliance_async(question: str):
    """
    Async wrapper for compliance validation to fit the async framework.
    """
    return validate_compliance(question)

async def show_compliance_report(si_data):
    """
    Asynchronously handle the compliance check and report display.
    """
    compliance_question = f"Are there any compliance issues with the following shipping instruction: {si_data}?"

    # Use RAG pipeline to validate the fetched SI data for compliance asynchronously
    with st.spinner("Validating shipping instruction for compliance..."):
        try:
            # Fetch the compliance report asynchronously
            compliance_report = await validate_compliance_async(compliance_question)
            placeholder = st.empty()

            if compliance_report:
                # Assuming the compliance report is a generator or an iterable, handle streaming the content
                streamed_text = ""
                async for chunk in compliance_report:
                    if chunk is not None:
                        streamed_text = streamed_text + chunk
                        placeholder.info(streamed_text)
            else:
                st.error("No relevant compliance information found.")
        except Exception as e:
            st.error(f"An error occurred during compliance verification: {e}")

def show_validation_check_page():
    st.title("Compliance Validation Check")

    # Check if 'si_data' is in session state
    if "si_data" not in st.session_state:
        st.error("No Shipping Instruction data found. Please perform a search first.")
        return

    # Display the Shipping Instruction data
    si_data = st.session_state["si_data"]
    # st.subheader("Shipping Instruction Data:")
    # st.write(si_data)

    # Button to initiate compliance validation
    if st.button("Run Validation Check"):
        # Start the async function to show the compliance report
        asyncio.run(show_compliance_report(si_data))
        st.success("Validation check completed!")