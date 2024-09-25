import streamlit as st
from utils.mongo import fetch_shipping_instruction
from utils.nodes import *
from langgraph.graph import StateGraph, END
    
workflow = StateGraph(State)

# Add nodes
workflow.add_node("check_parties", check_parties)
workflow.add_node("validate_compliance", validate_compliance)
workflow.add_node("search_news", search_news)
workflow.add_node("generate_summary", generate_summary)

# Add edges
workflow.set_entry_point("check_parties")
workflow.add_edge("check_parties", "validate_compliance")
workflow.add_edge("validate_compliance", "search_news")
workflow.add_edge("search_news", "generate_summary")
workflow.add_edge("generate_summary", END)

graph = workflow.compile()

def main():
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
            response = graph.invoke({"si_data":si_data})
            st.title("LLM Summary Report")
            st.info(response['summary_answer'])
        else:
            st.error("No Shipping Instruction found for the provided Booking Reference.")

# Run the streamlit function
if __name__ == "__main__":
    main()
