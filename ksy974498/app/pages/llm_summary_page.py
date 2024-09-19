import streamlit as st
from utils.bill_of_lading import generate_bill_of_lading
from utils.openai_llm import llm

def show_llm_summary_page():
    st.title("LLM Summary Report")

    if "si_data" in st.session_state:
        si_data = st.session_state["si_data"]
        report = generate_bill_of_lading(si_data)
        
        if st.button("Generate LLM Enhanced Report"):
            enhanced_report = llm.predict(text=report)
            st.text_area("LLM Enhanced Report", enhanced_report, height=400)
    else:
        st.warning("Please search for a Shipping Instruction first.")
