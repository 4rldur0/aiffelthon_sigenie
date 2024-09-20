import streamlit as st
from pages import search_page, report_page, llm_summary_page
from pages.json_bl import main as display_report


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

if __name__ == "__main__":
    main()