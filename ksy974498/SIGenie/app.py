import streamlit as st

st.set_page_config(layout="wide")

from st_pages import search_page, report_page, llm_summary_page, validation_check_page, summary_page
from pages import json_bkg, json_bl, json_si, load_bl



def main():
    st.sidebar.title("Navigation")

    app_mode = st.sidebar.selectbox("Choose a mode", 
                                    ["Search", "Bill of Lading Report", "LLM Summary Report","Summary Report", "Validation Check Report"])

    if app_mode == "Search":
        search_page.show_search_page()
    elif app_mode == "Bill of Lading Report":
        report_page.show_report_page()
    elif app_mode == "LLM Summary Report":
        llm_summary_page.show_llm_summary_page()
    elif app_mode == "Summary Report":
        summary_page.main()
    elif app_mode == "Validation Check Report":
        validation_check_page.show_validation_check_page()

    # Footer 추가
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; padding: 10px;'>"
        "Copyright © 2024 SIGenie 0.02 - Early Access Version. All rights reserved."
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()