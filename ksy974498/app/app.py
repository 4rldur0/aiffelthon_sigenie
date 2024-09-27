import streamlit as st
from utils.mongo import fetch_shipping_instruction
from utils.modules import *
from utils.summary_model import show_summary_report
import asyncio

# Run 3 async chains
# ====== RAG 부분 추가해야 함 ========
async def check_async():
    si_data = st.session_state["si_data"]
    outputs = await asyncio.gather(
        check_parties(si_data),
        search_news(si_data)
    )
    return outputs

def run_async_function(async_func, *args):
    """
    Helper to run async functions synchronously using asyncio.run().
    """
    return asyncio.run(async_func(*args))
  
# The main function where Streamlit interacts with the user
def main():
    # Input field for entering the booking reference
    booking_reference = st.text_input("Enter Booking Reference")

    if st.button("Search"):
        # Fetch the shipping instruction data from MongoDB
        si_data = fetch_shipping_instruction(booking_reference)

        if si_data:
            # Save the fetched SI data in Streamlit's session state
            st.session_state["si_data"] = si_data
            st.success("Shipping Instruction found!")

            # Run the async task using the sync wrapper
            sources = run_async_function(check_async)
            
            st.title("LLM Summary Report")
            box = st.empty()
            
            # Generate the summary using async function wrapped in sync function
            show_summary_report(sources)
            # run_async_function(, box, sources)
        else:
            st.error("No Shipping Instruction found for the provided Booking Reference.")

# Run the app
if __name__ == "__main__":
    main()