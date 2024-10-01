# Import Libraries
import streamlit as st
import datetime
import logging
from compliance_pipeline import validate_compliance  # Import the compliance validation pipeline

# Set up logging for error tracking
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

def run():
    # Initialize session state for storing chat messages
    if "booking_messages" not in st.session_state:
        st.session_state.booking_messages = []

    # Display chat messages from the session state
    for message in st.session_state.booking_messages:
        with st.chat_message(message["role"]):
            st.markdown(f"{message['content']}\n\n<div style='font-size:0.8em; color:#888;'>{message['timestamp']}</div>", unsafe_allow_html=True)

    # Capture user input
    prompt = st.chat_input("Any question about Compliance?")

    if prompt:
        # Save the user message in session state
        user_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.booking_messages.append({"role": "user", "content": prompt, "timestamp": user_timestamp})

        # Display the user message in the UI
        with st.chat_message("user"):
            st.markdown(f"{prompt}\n\n<div style='font-size:0.8em; color:#888;'>{user_timestamp}</div>", unsafe_allow_html=True)

        # Generate a response for the user input
        with st.spinner("Thinking..."):
            try:
                response = validate_compliance(prompt)
                ai_response = response if isinstance(response, str) else response.get("generation", "No response generated")
                ai_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Save and display the AI response in session state
                st.session_state.booking_messages.append({"role": "assistant", "content": ai_response, "timestamp": ai_timestamp})
                with st.chat_message("assistant"):
                    st.markdown(f"{ai_response}\n\n<div style='font-size:0.8em; color:#888;'>{ai_timestamp}</div>", unsafe_allow_html=True)
            except RuntimeError as e:
                st.error(f"An error occurred: {e}")
                logging.error(f"RuntimeError in compliance validation: {e}")
            except Exception as e:
                st.error("An unexpected error occurred. Please try again later.")
                logging.error(f"Unexpected error: {e}")

        st.rerun()

# Main entry point for the Streamlit app
if __name__ == "__main__":
    run()
