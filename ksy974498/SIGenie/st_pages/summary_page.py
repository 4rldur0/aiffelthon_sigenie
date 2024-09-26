import streamlit as st
import asyncio
from .report_page import display_bl_form, show_report_page
from .llm_summary_page import show_llm_summary_page

# Main function to display both pages side by side
def main():
    # Split the screen into two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Bill of Lading Report")
        show_report_page()

    with col2:
        st.header("LLM Summary Report")
        show_llm_summary_page()

if __name__ == "__main__":
    main()