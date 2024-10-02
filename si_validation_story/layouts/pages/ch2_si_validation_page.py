import streamlit as st
from ._page_templates import BLDraftPage
from graphs.si_validation_graph import SIValidation

graph = SIValidation()

def generate_summary(summary_result):
    with st.spinner("Running..."):
        placeholder = st.empty()
        try:
            streamed_text = ''
            for chunk in summary_result:
                if chunk is not None:
                    streamed_text += chunk
                    placeholder.info(streamed_text)
        except Exception as e:
            st.error(f"An error occurred while generating the summary: {e}")

def main():
    graph.state["si_data"] = st.session_state["si_data"]

    st.title("Ch 2: Sipping Instruction Validation")
    result = None
    if st.button("Generate Report"):
        try:
            result = graph.invoke()
        except Exception as e:
            st.error(f"An error occurred while Searching the shipping Instruction: {str(e)}")
            st.stop()

    if result is not None:
        si_data = result.get("si_data")
        if si_data:
            bl_draft_page = BLDraftPage(si_data=si_data)

            # Split the screen into two columns
            col1, col2 = st.columns(2)

            with col1:
                bl_draft_page.show_bl_draft_page()
            with col2:
                st.title("Shipping Instruction Validation Report")
                generate_summary(result.get("summary_answer", "No summary available"))
        else:
            st.warning("No shipping instruction data found for the given booking reference.")