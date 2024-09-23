import streamlit as st
from pages import search_page, report_page, llm_summary_page
from pages import json_bkg, json_bl, json_si
from pages.load_bl import main as display_report


def main():
    st.sidebar.title("Navigation")

    app_mode = st.sidebar.selectbox("Choose a mode", ["Search", "Bill of Lading Report", "Report Page", "LLM Summary Report"])

    if app_mode == "Search":
        search_page.show_search_page()
    elif app_mode == "Bill of Lading Report":
        report_page.show_report_page()
    elif app_mode == "Report Page":
        display_report()
    elif app_mode == "LLM Summary Report":
        llm_summary_page.show_llm_summary_page()


        # Sidebar menu
    menu = st.sidebar.selectbox(
        "Select Document Type",
        ["Booking", "Shipping Instructions", "Bill of Lading"]
    )

    # Main content
    if menu == "Booking":
        st.title("SIGenie Booking")
        json_bkg.main()
    elif menu == "Shipping Instructions":
        st.title("SIGenie Shipping Instructions")
        json_si.main()
    elif menu == "Bill of Lading":
        st.title("SIGenie Bill of Lading")
        json_bl.main()  # Changed from JSON_BL to json_bl

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