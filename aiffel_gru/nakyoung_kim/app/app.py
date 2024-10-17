import streamlit as st
from utils.mongo import fetch_shipping_instruction
from utils.modules import *
import asyncio
       
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
            start_time = time.time()
            outputs = await asyncio.gather(
                check_parties(si_data),
                validate_compliance(si_data),
                search_news(si_data)
            )
            print(f"All tasks completed in {time.time() - start_time} seconds")
            st.title("LLM Summary Report")
            box = st.empty()
            generate_summary(box, outputs)
            print(f"Summary completed in {time.time() - start_time} seconds")
        else:
            st.error("No Shipping Instruction found for the provided Booking Reference.")

# Run the streamlit function
if __name__ == "__main__":
    asyncio.run(main())
