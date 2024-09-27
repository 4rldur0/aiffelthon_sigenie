import streamlit as st
from utils.mongo import fetch_shipping_instruction

def show_search_page():
    st.title("Search for Shipping Instruction")

    # Input field to enter the booking reference
    booking_reference = st.text_input("Enter Booking Reference")

    if st.button("Search"):
        # Fetch the SI data from MongoDB
        si_data = fetch_shipping_instruction(booking_reference)

        if si_data:
            # Save SI data in session state for use in the validation check page
            st.session_state["si_data"] = si_data
            st.success("Shipping Instruction found!")
            
        else:
            st.error("No Shipping Instruction found for the provided Booking Reference.")