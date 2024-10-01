import streamlit as st
from ._page_templates import SearchPage, BLDraftPage, SummaryPage
from graphs.si_validation_graph import SIValidation

# Main function to display both pages side by side
def main():
    # Split the screen into two columns
    col1, col2 = st.columns(2)

    search_page = SearchPage()
    bl_draft_page = BLDraftPage()
    summary_graph = SIValidation()
    summary_page = SummaryPage(chapter_name="Ch2: Shipping Instrunction Validation", graph=summary_graph)
    
    with col1:
        search_page.show_search_page()
        if st.session_state["si_data"]:
            bl_draft_page.show_bl_draft_page()

    with col2:
        summary_page.show_summary_page()