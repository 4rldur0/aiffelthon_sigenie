import streamlit as st
from utils.mongo import fetch_shipping_instruction
from utils.rag_pipeline import validate_compliance
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

def show_search_page():
    st.title("Search for Shipping Instruction")

    # Input field to enter the booking reference
    booking_reference = st.text_input("Enter Booking Reference")

    if st.button("Search"):
        # Fetch the SI data from MongoDB
        si_data = fetch_shipping_instruction(booking_reference)

        if si_data:
            st.session_state["si_data"] = si_data
            st.success("Shipping Instruction found! Go to 'Bill of Lading Report' to view.")
            
            st.subheader("Validation Report:")
            # Start the async function to show the compliance report
            asyncio.run(show_compliance_report(si_data))
            st.success("Validation check completed!")
        else:
            st.error("No Shipping Instruction found for the provided Booking Reference.")
