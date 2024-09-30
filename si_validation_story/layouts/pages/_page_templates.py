import streamlit as st
import base64

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# ========= 수정 필요 ==========
class SearchPage:
    def fetch_shipping_instruction(self, booking_reference):
        # Load environment variables from .env file
        load_dotenv()

        # Set up MongoDB connection using environment variables
        MONGO_URI = os.getenv("MONGODB_URI")
        DB_NAME = os.getenv("MONGODB_DB_NAME")
        COLLECTION_NAME = "si"  # Collection storing shipping instructions

        # Create MongoDB client and connect to the specific database and collection
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        """
        Fetch the shipping instruction from MongoDB based on the booking reference.
        """
        return collection.find_one({'bookingReference': booking_reference})

    def show_search_page(self):
        st.title("Search for Shipping Instruction")

        # Input field to enter the booking reference
        booking_reference = st.text_input("Enter Booking Reference")

        if st.button("Search"):
            # Fetch the SI data from MongoDB
            si_data = self.fetch_shipping_instruction(booking_reference)

            if si_data:
                # Save SI data in session state for use in the validation check page
                st.session_state["si_data"] = si_data
                st.success("Shipping Instruction found!")
                
            else:
                st.error("No Shipping Instruction found for the provided Booking Reference.")

class BLDraftPage:
    def __init__(self):
        self.logo_img = "./layouts/imgs/containergenie.png"
        # Custom CSS to style the Bill of Lading
        self.custom_css = """
        <style>
        @font-face {
            font-family: 'Freesentation';
            src: url('./ui/fonts/Freesentation.ttf') format('truetype');
        }
        html, body, [class*="st-"] {
            font-family: 'Freesentation', sans-serif;
        }
            .bl-form {
                font-family: Arial, sans-serif;
                border: 2px solid black;
                padding: 10px;
                margin-bottom: 20px;
                width: 100%;
            }
            .bl-header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                border-bottom: 1px solid black;
                padding-bottom: 10px;
                margin-bottom: 10px;
            }
            .bl-title {
                margin-right: 30px;
            }
            .bl-section {
                margin-bottom: 10px;
                border: 1px solid black;
                padding: 5px;
            }
            .bl-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }
            .bl-footer {
                border-top: 1px solid black;
                padding-top: 10px;
                margin-top: 10px;
            }
            .bl-logo {
                text-align: right;
                margin-left: auto;
            }
            .bl-logo img {
                max-width: 250px;
                height: auto;
            }
            .bl-table {
                width: 100%;
                border-collapse: collapse;
            }
            .bl-table th, .bl-table td {
                border: 1px solid black;
                padding: 5px;
                text-align: left;
            }
        </style>
        """

    def get_base64_encoded_image(self, image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    def generate_container_rows(self, containers, doc):
        particulars_html = f"""
        <h3>PARTICULARS FURNISHED BY SHIPPER - CARRIER NOT RESPONSIBLE</h3>
        <table class="bl-table">
            <tr>
                <th>MARKS AND NUMBERS</th>
                <th>NO. OF CONTAINERS OR PACKAGES</th>
                <th>DESCRIPTION OF GOODS</th>
                <th>GROSS WEIGHT</th>
                <th>MEASUREMENT</th>
            </tr>
        """
        container_info_html = f"""
        <h3>TOTAL No. OF CONTAINERS OR PACKAGES RECEIVED BY THE CARRIER</h3>
        <table class="bl-table">
            <tr>
                <th>CONTAINER NUMBERS</th>
                <th>SEAL NUMBERS</th>
                <th>SIZE</th>
                <th>TYPE</th>
            </tr>
        """
        footer_info_html = f"""
        <p><strong>Freight Payable at:</strong> {doc['paymentDetails']['freightPayableAt']}</p>
        <p><strong>Number of Original B/Ls:</strong> {doc['documentationDetails']['numberOfOriginalBLs']}</p>
        <p><strong>Place of Issue:</strong> {doc['paymentDetails']['freightPayableAt']}</p>
        <p><strong>Date of Issue:</strong> {doc['additionalInformation']['onboardDate']}</p>
        """
        
        for container in containers:
            particulars_html += f"""
            <tr>
                <td>{container.get('marksAndNumbers', '')}</td>
                <td>{container.get('numberOfPackages', '')}</td>
                <td>{container.get('descriptionOfGoods', '')}</td>
                <td>{container.get('grossWeight', '')}</td>
                <td>{container.get('measurement', '')}</td>
            </tr>
            """
            container_info_html += f"""
            <tr>
                <td>{container.get('containerNumber', '')}</td>
                <td>{container.get('sealNumber', '')}</td>
                <td>{container.get('containerSize', '')}</td>
                <td>{container.get('containerType', '')}</td>
            </tr>
            """

        particulars_html += "</table>"
        container_info_html += "</table>"
        return particulars_html, container_info_html, footer_info_html   
    def display_bl_form(self, doc):
        # Apply custom CSS
        st.markdown(self.custom_css, unsafe_allow_html=True)
        
        # Load and encode the logo
        logo_base64 = self.get_base64_encoded_image(self.logo_img)
        
        # Generate container information HTML
        particulars_html, container_info_html, footer_info_html = self.generate_container_rows(doc['containers'], doc)

        # Create the BL form HTML
        bl_html = f"""
        <div class="bl-form">
            <div class="bl-header">
                <div class="bl-title">
                    <h2>BILL OF LADING (B/L)(Draft)</h2>
                </div>
                <div>
                    <p class="bl-row"><strong>Booking Number:</strong> {doc.get('bookingReference', '')}</p>
                    <p class="bl-row"><strong>Service Type:</strong> {doc.get('service', '')}</p>
                    <p class="bl-row"><strong>B/L Number:</strong> {doc.get('bookingReference', '')}</p>
                </div>
                <div class="bl-logo">
                    <img src="data:image/jpeg;base64,{logo_base64}" alt="Company Logo">
                </div>
            </div>
            <div class="bl-section">
                <h3>SHIPPER / EXPORTER (Full Name and Address)</h3>
                <p class="bl-row">{doc.get('partyDetails', {}).get('shipper', {}).get('name', '')}</p>
                <p class="bl-row">{doc.get('partyDetails', {}).get('shipper', {}).get('address', '')}</p>
                <p class="bl-row">Tel: {doc.get('partyDetails', {}).get('shipper', {}).get('telephone', '')}</p>
            </div>
            <div class="bl-section">
                <h3>CONSIGNEE (Full Name and Address)</h3>
                <p class="bl-row">{doc.get('partyDetails', {}).get('consignee', {}).get('name', '')}</p>
                <p class="bl-row">{doc.get('partyDetails', {}).get('consignee', {}).get('address', '')}</p>
                <p class="bl-row">Tel: {doc.get('partyDetails', {}).get('consignee', {}).get('telephone', '')}</p>
            </div>
            <div class="bl-section">
                <h3>NOTIFY PARTY (Full Name and Address)</h3>
                <p class="bl-row">{doc.get('partyDetails', {}).get('notifyParty', {}).get('name', '')}</p>
                <p class="bl-row">{doc.get('partyDetails', {}).get('notifyParty', {}).get('address', '')}</p>
                <p class="bl-row">Tel: {doc.get('partyDetails', {}).get('notifyParty', {}).get('telephone', '')}</p>
            </div>
            <div class="bl-grid">
                <div class="bl-section">
                    <h3>PLACE OF RECEIPT</h3>
                    <p class="bl-row">{doc.get('routeDetails', {}).get('placeOfReceipt', '')}</p>
                </div>
                <div class="bl-section">
                    <h3>PORT OF LOADING</h3>
                    <p class="bl-row">{doc.get('routeDetails', {}).get('portOfLoading', '')}</p>
                </div>
            </div>
            <div class="bl-grid">
                <div class="bl-section">
                    <h3>PORT OF DISCHARGE</h3>
                    <p class="bl-row">{doc.get('routeDetails', {}).get('portOfDischarge', '')}</p>
                </div>
                <div class="bl-section">
                    <h3>PLACE OF DELIVERY</h3>
                    <p class="bl-row">{doc.get('routeDetails', {}).get('placeOfDelivery', '')}</p>
                </div>
            </div>
            <div class="bl-grid">
                <div class="bl-section">
                    <h3>VESSEL NAME</h3>
                    <p class="bl-row">{doc.get('voyageDetails', {}).get('vesselName', '')}</p>
                </div>
                <div class="bl-section">
                    <h3>VOYAGE NUMBER</h3>
                    <p class="bl-row">{doc.get('voyageDetails', {}).get('voyageNumber', '')}</p>
                </div>
            </div>

        <div class="bl-section">
            {particulars_html}
        </div>
        <div class="bl-section">
            {container_info_html}
        </div>
        <div class="bl-section">
            {footer_info_html}
        </div>
        <div class="bl-footer">
            <p class="small-text">The number of containers of packages shown in the 'TOTAL No. OF CONTAINERS OR PACKAGES RECEIVED BY THE CARRIER's box which are said by the shipper to hold or consolidate the goods described in the PARTICULARS FURNISHED BY SHIPPER - CARRIER NOT RESPONSIBLE box, have been received by CHERRY SHIPPING LINE from the shipper in apparent good order and condition except as otherwise indicated hereon - weight, measure, marks, numbers, quality, quantity, description, contents and value unknown - for Carriage from the Place of Receipt or the Port of loading (whichever is applicable) to the Port of Discharge or the Place of Delivery (whichever is applicable) on the terms and conditions hereof INCLUDING THE TERMS AND CONDITIONS ON THE REVERSE SIDE HEREOF, THE CARRIER'S APPLICABLE TARIFF AND THE TERMS AND CONDITIONS OF THE PRECARRIER AND ONCARRIER AS APPLICABLE IN ACCORDANCE WITH THE TERMS AND CONDITIONS ON THE REVERSE SIDE HEREOF.</p>
            <p class="small-text">IN WITNESS WHEREOF {doc['documentationDetails']['numberOfOriginalBLs']} ({doc['documentationDetails']['numberOfOriginalBLs']} in words) ORIGINAL BILLS OF LADING (unless otherwise stated above) HAVE BEEN SIGNED ALL OF THE SAME TENOR AND DATE, ONE OF WHICH BEING ACCOMPLISHED THE OTHER(S) TO STAND VOID.</p>
            <div class="bl-grid">
                <div>
                    <p class="bl-row"><strong>CHERRY SHIPPING LINE</strong></p>
                    <p class="bl-row"><strong>as Carrier</strong></p>
                    <p class="bl-row">By ContainerGenie.ai CO., LTD.</p>
                    <p>as Agents only for Carrier</p>
                </div>
                <div>
                    <p class="bl-row"><strong>Place Issued: {doc['paymentDetails']['freightPayableAt']}</strong></p>
                    <p class="bl-row"><strong>Date Issued: {doc['additionalInformation']['onboardDate']}</strong></p>
                </div>
            </div>
        </div>
        """
        
        # Render the BL form
        st.html(bl_html)

    def show_bl_draft_page(self):
        st.title("Bill of Lading Report Draft")
        
        if "si_data" in st.session_state:
            si_data = st.session_state["si_data"]
            self.display_bl_form(si_data)
        else:
            st.warning("Please search for a Shipping Instruction first.")
      

class SummaryPage:
    def __init__(self, chapter_name, graph):
        self.chapter_name = chapter_name
        self.graph = graph
    
    def generate_summary(self, si_data):
        with st.spinner("Running..."):
            try:
                self.graph.invoke()
            except Exception as e:
                st.error(f"An error occurred while generating the summary: {e}")
        
    def show_summary_page(self):
        st.title(self.chapter_name)

        # Check if 'si_data' is present in session state
        if "si_data" not in st.session_state:
            st.error("No Shipping Instruction data found. Please perform a search first.")
            return

        # Retrieve the SI data from session state
        si_data = st.session_state["si_data"]

        # Button to initiate the validation check
        if st.button("Run"):
            # Run the asynchronous summary generation function
            self.generate_summary(si_data)
            st.success("Summary completed!")
        else:
            st.warning("Please search for a Shipping Instruction first.")