import streamlit as st
from utils.bill_of_lading import generate_bill_of_lading

def show_report_page():
    st.title("Bill of Lading Report")
    
    if "si_data" in st.session_state:
        si_data = st.session_state["si_data"]
        report = generate_bill_of_lading(si_data)
        st.text_area("Bill of Lading Report", report, height=500)
    else:
        st.warning("Please search for a Shipping Instruction first.")
