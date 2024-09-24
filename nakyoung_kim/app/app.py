import streamlit as st
from utils.mongo import fetch_shipping_instruction
from utils.modules import *
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
       
async def main():
    # Input field to enter the booking reference
    booking_reference = st.text_input("Enter Booking Reference")

    if st.button("Search"):
        # Fetch the SI data from MongoDB
        si_data = fetch_shipping_instruction(booking_reference)

        if si_data:
            # Save SI data in session state for use in the validation check page
            st.session_state["si_data"] = si_data
            st.success("Shipping Instruction found!")

            # After successful search, run async check
            outputs = await asyncio.gather(
                check_parties(si_data),
                search_news(si_data)
            )
            st.title("LLM Summary Report")
            box = st.empty()
            generate_summary(box, outputs)
        else:
            st.error("No Shipping Instruction found for the provided Booking Reference.")

# Run the streamlit function
if __name__ == "__main__":
    asyncio.run(main())
