import streamlit as st
import os
import base64

# Set page config (this should be the first Streamlit command)
st.set_page_config(layout="wide", page_title="Shipping Document Viewer")

# Function to get base64 encoded font
def get_base64_encoded_font(font_path):
    with open(font_path, "rb") as font_file:
        return base64.b64encode(font_file.read()).decode('utf-8')

# Load and encode the Freesentation font
font_base64 = get_base64_encoded_font("./fonts/Freesentation.ttf")

# Apply custom font
custom_font_css = f"""
<style>
@font-face {{
    font-family: 'Freesentation';
    src: url(data:font/ttf;base64,{font_base64}) format('truetype');
}}

* {{
    font-family: 'Freesentation', sans-serif !important;
}}
</style>
"""
st.markdown(custom_font_css, unsafe_allow_html=True)

# Import modules after setting page config
import json_bkg
import json_si
import json_bl 

def main():
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
        json_bl.main()

    # Footer 추가
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; padding: 10px;'>"
        "Copyright © 2024 SIGenie 0.03 - Early Access Version. All rights reserved."
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()