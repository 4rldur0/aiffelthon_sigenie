import streamlit as st
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import base64

# Load environment variables and set up MongoDB connection
load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")
COLLECTION_NAME = "si"  # Changed from "bl" to "si"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Custom CSS to style the BL form
custom_css = """
<style>
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

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def display_bl_form(doc):
    # Load and encode the logo
    logo_base64 = get_base64_encoded_image("./img/containergenie.png")
    
    # Generate container rows
    container_info_html = generate_container_rows(doc['containers'], doc)

    # Create the BL form HTML
    bl_html = f"""
    <div class="bl-form">
        <div class="bl-header">
            <div>
                <h2>BILL OF LADING</h2>
            </div>
            <div>
                <p><strong>BOOKING NO:</strong> {doc.get('bookingReference', '')}</p>
                <p><strong>SERVICE:</strong> {doc.get('service', '')}</p>
                <p><strong>BL NO:</strong> {doc.get('bookingReference', '')}</p>
            </div>
            <div class="bl-logo">
                <img src="data:image/jpeg;base64,{logo_base64}" alt="Company Logo">
            </div>
        </div>
        <div class="bl-section">
            <h3>SHIPPER (NAME AND FULL ADDRESS)</h3>
            <p>{doc.get('partyDetails', {}).get('shipper', {}).get('name', '')}</p>
            <p>{doc.get('partyDetails', {}).get('shipper', {}).get('address', '')}</p>
            <p>Tel: {doc.get('partyDetails', {}).get('shipper', {}).get('telephone', '')}</p>
        </div>
        <div class="bl-section">
            <h3>CONSIGNEE (NAME AND FULL ADDRESS)</h3>
            <p>{doc.get('partyDetails', {}).get('consignee', {}).get('name', '')}</p>
            <p>{doc.get('partyDetails', {}).get('consignee', {}).get('address', '')}</p>
            <p>Tel: {doc.get('partyDetails', {}).get('consignee', {}).get('telephone', '')}</p>
        </div>
        <div class="bl-section">
            <h3>NOTIFY PARTY (NAME AND ADDRESS)</h3>
            <p>{doc.get('partyDetails', {}).get('notifyParty', {}).get('name', '')}</p>
            <p>{doc.get('partyDetails', {}).get('notifyParty', {}).get('address', '')}</p>
            <p>Tel: {doc.get('partyDetails', {}).get('notifyParty', {}).get('telephone', '')}</p>
        </div>
        <div class="bl-grid">
            <div class="bl-section">
                <h3>PLACE OF RECEIPT BY PRE-CARRIER</h3>
                <p>{doc.get('routeDetails', {}).get('placeOfReceipt', '')}</p>
            </div>
            <div class="bl-section">
                <h3>PORT OF LOADING</h3>
                <p>{doc.get('routeDetails', {}).get('portOfLoading', '')}</p>
            </div>
        </div>
        <div class="bl-grid">
            <div class="bl-section">
                <h3>VESSEL</h3>
                <p>{doc.get('voyageDetails', {}).get('vesselName', '')}</p>
            </div>
            <div class="bl-section">
                <h3>PORT OF DISCHARGE</h3>
                <p>{doc.get('routeDetails', {}).get('portOfDischarge', '')}</p>
            </div>
        </div>
    <div class="bl-section">
        <h3>PARTICULARS FURNISHED BY SHIPPER - CARRIER NOT RESPONSIBLE</h3>
        {container_info_html}
    </div>
    <div class="bl-footer">
        <div class="bl-grid">
            <div>
                <p><strong>FCL/FCL</strong></p>
                <p><strong>{doc['shippingTerm']}</strong></p>
            </div>
            <div>
                <p><strong>"{doc['paymentDetails']['freightPaymentTerms'].upper()}"</strong></p>
                <p>{doc['totalShipment']['totalContainers']}</p>
            </div>
        </div>
        <p><strong>TOTAL No. OF CONTAINERS OF PACKAGES RECEIVED BY THE CARRIER: {doc['totalShipment']['totalContainers']}</strong></p>
        <!-- Additional footer content -->
    </div>
    """
    
    # Use st.components.v1.html for more complex HTML rendering
    st.components.v1.html(custom_css + bl_html, height=800, scrolling=True)

def generate_container_rows(containers, doc):
    table_html = f"""
    <table class="bl-table">
        <tr>
            <th>MARKS AND NUMBERS</th>
            <th>NO. OF PKGS.</th>
            <th>DESCRIPTION OF PACKAGES AND GOODS</th>
            <th>GROSS WEIGHT (KG)</th>
            <th>MEASUREMENT (CBM)</th>
        </tr>
    """

    for container in containers:
        table_html += f"""
        <tr>
            <td>{container.get('marksAndNumbers', '')}</td>
            <td>{doc['totalShipment']['totalPackages']} {container.get('packageType', '')}</td>
            <td>{doc.get('commodityDescription', '')}</td>
            <td>{doc['totalShipment'].get('totalGrossWeight', '')}</td>
            <td>{doc['totalShipment'].get('totalMeasurement', '')}</td>
        </tr>
        """

    table_html += """
    </table>
    <h3>CONTAINER INFORMATION</h3>
    <table class="bl-table">
        <tr>
            <th>Container No.</th>
            <th>Seal No.</th>
            <th>No. of Pkgs</th>
            <th>Description</th>
            <th>Gross Weight (KG)</th>
            <th>Measurement (CBM)</th>
        </tr>
    """
    
    for container in containers:
        table_html += f"""
        <tr>
            <td>{container.get('containerNumber', '')}</td>
            <td>{container.get('sealNumber', '')}</td>
            <td>{container.get('numberOfPackages', '')} {container.get('packageType', '')}</td>
            <td>SHIPPER'S LOAD, COUNT & WEIGHT, SOTW & SEAL SAID TO CONTAIN: {container.get('cargoDescription', '')}</td>
            <td>{container.get('grossWeight', '')}</td>
            <td>{container.get('measurement', '')}</td>
        </tr>
        """
    table_html += "</table>"
    return table_html

def main():
    st.title("BL Viewer")

    # Fetch all documents from MongoDB's si collection
    documents = list(collection.find())

    # Create a list of booking references
    booking_refs = [doc.get('bookingReference', 'Unknown') for doc in documents]
    
    # Create a selectbox for choosing a document by booking reference
    selected_booking_ref = st.selectbox(
        "Select a BL document",
        options=booking_refs,
        format_func=lambda x: f"Booking Ref: {x}"
    )

    # Find the selected document
    selected_doc = next((doc for doc in documents if doc.get('bookingReference') == selected_booking_ref), None)

    # Display the selected document as a BL form
    if selected_doc:
        display_bl_form(selected_doc)
    else:
        st.warning("No document found for the selected booking reference.")

if __name__ == "__main__":
    main()