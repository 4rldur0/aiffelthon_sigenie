from layouts.pages import ch1_si_intake_page, ch2_si_validation_page
import streamlit as st

st.set_page_config(layout="wide")

def main():
    st.sidebar.title("Chapters")

    app_mode = st.sidebar.selectbox("Choose a chapter", 
                                    ["Ch 1: Shipping Instruction Intake", "Ch 2: Shipping Instruction Validation"])

    if app_mode == "Ch 1: Shipping Instruction Intake":
        ch1_si_intake_page.main()
    elif app_mode == "Ch 2: Shipping Instruction Validation":
        ch2_si_validation_page.main()

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