import os
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # Ensure langchain and OpenAI package is installed

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

# Initialize OpenAI Chat Model (GPT-4)
llm = ChatOpenAI(model_name="gpt-4")

# Bill of Lading template for Shipping Instructions
b_l_template = """
# BILL OF LADING (B/L)

## SHIPPER / EXPORTER
{shipper_name}
{shipper_address}
Tel: {shipper_phone}

## CONSIGNEE
{consignee_name}
{consignee_address}
Tel: {consignee_phone}

## NOTIFY PARTY
{notify_name}
{notify_address}
Tel: {notify_phone}

## PLACE OF RECEIPT
{place_of_receipt}

## PORT OF LOADING
{port_of_loading}

## PORT OF DISCHARGE
{port_of_discharge}

## PLACE OF DELIVERY
{place_of_delivery}

## VESSEL NAME
{vessel_name}

## VOYAGE NUMBER
{voyage_number}

## PARTICULARS FURNISHED BY SHIPPER - CARRIER NOT RESPONSIBLE

### Marks and Numbers: 
{marks_numbers}

### Number of Packages: 
{num_of_packages}

### Description of Goods: 
{goods_description}

### Gross Weight (kg): 
{gross_weight}

### Measurement (CBM): 
{measurement_cbm}

## CONTAINER INFORMATION
Container No. | Seal No. | Number of Packages | Gross Weight (kg) | Measurement (CBM)
{container_info}

## TOTAL NUMBER OF CONTAINERS/PACKAGES RECEIVED BY THE CARRIER
{total_containers_packages}
"""

def fetch_shipping_instruction(booking_reference):
    """
    Fetch the shipping instruction from MongoDB based on the booking reference.
    """
    return collection.find_one({'bookingReference': booking_reference})

def generate_bill_of_lading(si_data):
    """
    Generate a bill of lading based on the provided SI data.
    """
    # Extract details from the shipping instruction data
    shipper_name = si_data.get('partyDetails', {}).get('shipper', {}).get('name', 'N/A')
    shipper_address = si_data.get('partyDetails', {}).get('shipper', {}).get('address', 'N/A')
    shipper_phone = si_data.get('partyDetails', {}).get('shipper', {}).get('phone', 'N/A')

    consignee_name = si_data.get('partyDetails', {}).get('consignee', {}).get('name', 'N/A')
    consignee_address = si_data.get('partyDetails', {}).get('consignee', {}).get('address', 'N/A')
    consignee_phone = si_data.get('partyDetails', {}).get('consignee', {}).get('phone', 'N/A')

    notify_name = si_data.get('partyDetails', {}).get('notifyParty', {}).get('name', 'N/A')
    notify_address = si_data.get('partyDetails', {}).get('notifyParty', {}).get('address', 'N/A')
    notify_phone = si_data.get('partyDetails', {}).get('notifyParty', {}).get('phone', 'N/A')

    place_of_receipt = si_data.get('placeOfReceipt', 'N/A')
    port_of_loading = si_data.get('portOfLoading', 'N/A')
    port_of_discharge = si_data.get('portOfDischarge', 'N/A')
    place_of_delivery = si_data.get('placeOfDelivery', 'N/A')

    vessel_name = si_data.get('vessel', {}).get('name', 'N/A')
    voyage_number = si_data.get('vessel', {}).get('voyageNumber', 'N/A')

    marks_numbers = si_data.get('marksNumbers', 'N/A')
    num_of_packages = si_data.get('totalShipment', {}).get('totalPackages', 'N/A')
    goods_description = si_data.get('commodityDescription', 'N/A')
    gross_weight = si_data.get('containers', [{}])[0].get('grossWeight', 'N/A')
    measurement_cbm = si_data.get('containers', [{}])[0].get('measurement', 'N/A')

    container_info = ""
    containers = si_data.get('containers', [])
    for container in containers:
        container_info += f"{container.get('containerNumber', 'N/A')} | {container.get('sealNumber', 'N/A')} | {container.get('numPackages', 'N/A')} | {container.get('grossWeight', 'N/A')} | {container.get('measurement', 'N/A')}\n"

    total_containers_packages = f"{len(containers)} containers / {num_of_packages} packages"

    # Format the Bill of Lading report
    report = b_l_template.format(
        shipper_name=shipper_name,
        shipper_address=shipper_address,
        shipper_phone=shipper_phone,
        consignee_name=consignee_name,
        consignee_address=consignee_address,
        consignee_phone=consignee_phone,
        notify_name=notify_name,
        notify_address=notify_address,
        notify_phone=notify_phone,
        place_of_receipt=place_of_receipt,
        port_of_loading=port_of_loading,
        port_of_discharge=port_of_discharge,
        place_of_delivery=place_of_delivery,
        vessel_name=vessel_name,
        voyage_number=voyage_number,
        marks_numbers=marks_numbers,
        num_of_packages=num_of_packages,
        goods_description=goods_description,
        gross_weight=gross_weight,
        measurement_cbm=measurement_cbm,
        container_info=container_info,
        total_containers_packages=total_containers_packages
    )

    return report

def main():
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose a mode", ["Search", "Bill of Lading Report", "LLM Summary Report"])

    if app_mode == "Search":
        st.title("Search for Shipping Instruction")
        
        # Input field to enter the booking reference
        booking_reference = st.text_input("Enter Booking Reference")
        
        if st.button("Search"):
            # Fetch the SI data from MongoDB
            si_data = fetch_shipping_instruction(booking_reference)

            if si_data:
                st.session_state["si_data"] = si_data
                st.success("Shipping Instruction found! Go to 'Bill of Lading Report' to view.")
            else:
                st.error("No Shipping Instruction found for the provided Booking Reference.")
    
    elif app_mode == "Bill of Lading Report":
        st.title("Bill of Lading Report")
        
        if "si_data" in st.session_state:
            si_data = st.session_state["si_data"]
            report = generate_bill_of_lading(si_data)
            st.text_area("Bill of Lading Report", report, height=500)
        else:
            st.warning("Please search for a Shipping Instruction first.")
    
    elif app_mode == "LLM Summary Report":
        st.title("LLM Summary Report")

        if "si_data" in st.session_state:
            si_data = st.session_state["si_data"]
            report = generate_bill_of_lading(si_data)
            
            if st.button("Generate LLM Enhanced Report"):
                enhanced_report = llm.predict(text=report)  # Adjusted for chat model usage
                st.text_area("LLM Enhanced Report", enhanced_report, height=400)
        else:
            st.warning("Please search for a Shipping Instruction first.")

if __name__ == "__main__":
    main()
