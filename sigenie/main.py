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

/* 모든 Streamlit 컴포넌트에 대한 스타일 */
.stTextInput, .stSelectbox, .stMultiselect, .stDateInput, .stTimeInput,
.stNumber, .stText, .stMarkdown, .stTable, .stDataFrame, .stButton,
.stRadio, .stCheckbox, .stMetric, .stProgress, .stSlider, .stFileUploader,
.stImage, .stAudio, .stVideo, .stPlotly, .stVega, .stPydeck, .stMap,
.stCode, .stEcho, .stSpinner, .stBalloons, .stSuccess, .stInfo, .stWarning, .stError {{
    font-family: 'Freesentation', sans-serif !important;
}}

/* 헤더와 사이드바에 대한 스타일 */
.stSidebar, .stSidebar *, .stHeader, .stHeader * {{
    font-family: 'Freesentation', sans-serif !important;
}}

/* 모든 텍스트 요소에 대한 스타일 */
body, p, h1, h2, h3, h4, h5, h6, span, div {{
    font-family: 'Freesentation', sans-serif !important;
}}
</style>
"""
st.markdown(custom_font_css, unsafe_allow_html=True)

# Import modules after setting page config
import json_bkg
import json_si
import json_bl 
from search_booking import search_booking
from search_si import search_shipping_instructions

def main():
    # Sidebar menu
    menu = st.sidebar.selectbox(
        "Select Document Type",
        ["Booking", "Shipping Instructions", "Bill of Lading", "Booking Search", "Shipping Instruction Search"]
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
    elif menu == "Booking Search":
        st.title("Booking Search")
        query = st.text_input("Enter search query for Booking")
        if query:
            results = search_booking(query)
            for result in results:
                st.markdown(f"""
                <div style='font-family: Freesentation, sans-serif;'>
                <strong>Booking Reference:</strong> {result['bookingReference']}<br>
                <strong>Customer Name:</strong> {result['customerName']}<br>
                <strong>Container Count:</strong> {result['containerCount']}<br>
                <strong>Cargo Description:</strong> {result['chapterDescription']}<br>
                <strong>Similarity Score:</strong> {result['similarity']:.2f}
                </div>
                <hr>
                """, unsafe_allow_html=True)
    elif menu == "Shipping Instruction Search":
        st.title("Shipping Instruction Search")
        query = st.text_input("Enter search query for Shipping Instructions")
        if query:
            results = search_shipping_instructions(query)
            for result in results:
                st.markdown(f"""
                <div style='font-family: Freesentation, sans-serif;'>
                <strong>Booking Reference:</strong> {result['bookingReference']}<br>
                <strong>Shipper Name:</strong> {result['shipperName']}<br>
                <strong>Container Count:</strong> {result['containerCount']}<br>
                <strong>Cargo Description:</strong> {result['cargoDescription']}<br>
                <strong>Similarity Score:</strong> {result['similarity']:.2f}
                </div>
                <hr>
                """, unsafe_allow_html=True)

    # Footer 추가
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; padding: 10px; font-family: Freesentation, sans-serif;'>"
        "Copyright © 2024 SIGenie 0.03-5009 - Early Access Version. All rights reserved."
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()