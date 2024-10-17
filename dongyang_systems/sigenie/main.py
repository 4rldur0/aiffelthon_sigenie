import streamlit as st
import os
from app import json_bkg, json_si, json_bl, search_si, search_compliance, search_compliance_qe
from utils.helpers import get_custom_font_css
from pymongo import MongoClient
from datetime import datetime


# Set page config (this should be the first Streamlit command)
st.set_page_config(layout="wide", page_title="Booking, Shipping Instruction")

# Apply custom font
st.markdown(get_custom_font_css(), unsafe_allow_html=True)

# MongoDB connection setup
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_collection_info(collection_name):
    collection = db[collection_name]
    count = collection.count_documents({})
    latest_doc = collection.find_one(sort=[('_id', -1)])
    last_update = latest_doc['_id'].generation_time if latest_doc else None
    return count, last_update

def main():
    # Sidebar menu
    menu = st.sidebar.selectbox(
        "Select Menu",
        ["Booking", "Shipping Instructions", "Bill of Lading", "Shipping Instruction Search", "Company Policy Search", "Company Policy Search QE"]
    )

    # Dataset info in sidebar
    st.sidebar.markdown("---")
    bkg_count, bkg_last_update = get_collection_info('bkg')
    si_count, si_last_update = get_collection_info('si')

    bkg_info = (
        f"**Booking Dataset:**\n\n"
        f"Documents: {bkg_count:,}\n\n"
        f"Last Update: {bkg_last_update.strftime('%Y-%m-%d %H:%M:%S') if bkg_last_update else 'N/A'}"
    )
    st.sidebar.info(bkg_info)
    
    si_info = (
        f"**SI Dataset:**\n\n"
        f"Documents: {si_count:,}\n\n"
        f"Last Update: {si_last_update.strftime('%Y-%m-%d %H:%M:%S') if si_last_update else 'N/A'}"
    )
    st.sidebar.info(si_info)

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
    elif menu == "Shipping Instruction Search":
        st.title("Shipping Instruction Search")
        search_si.main()
    elif menu == "Company Policy Search":
        st.title("Company Policy Search")
        search_compliance.main()
    elif menu == "Company Policy Search QE":
        st.title("Company Policy Search Quary Expansion")
        search_compliance_qe.main()

    # Footer 추가
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; padding: 10px;'>"
        "Copyright © 2024 SIGenie 0.06-6036 - Early Access Version. All rights reserved."
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
