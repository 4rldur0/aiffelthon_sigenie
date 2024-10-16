import os
import json
import streamlit as st
import pymongo
from pymongo import MongoClient, InsertOne
from bson import ObjectId
from dotenv import load_dotenv
from utils.helpers import get_custom_font_css

# Load environment variables from .env file
load_dotenv()

# Set up MongoDB connection using environment variables
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")
COLLECTION_NAME = "si"

# Create MongoDB client and connect to the specific database and collection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

PROCESSED_FILES_JSON = './dataset/processed_si_files.json'

def load_processed_files():
    try:
        with open('processed_si_files.json', 'r') as f:
            return set(json.load(f))
    except (json.JSONDecodeError, FileNotFoundError):
        # 파일이 비어있거나 존재하지 않을 경우 빈 세트 반환
        return set()

def save_processed_files(processed_files):
    with open(PROCESSED_FILES_JSON, 'w') as f:
        json.dump(list(processed_files), f)

def load_json_files(directory):
    """
    Load all JSON files from the specified directory.
    
    Args:
    directory (str): Path to the directory containing JSON files.
    
    Returns:
    dict: A dictionary where keys are filenames and values are the loaded JSON data.
    """
    json_files = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                json_files[filename] = json.load(file)
    return json_files

def get_processed_files():
    return load_processed_files()

def save_new_documents(json_files):
    processed_files = load_processed_files()
    existing_refs = set(collection.distinct('bookingReference'))
    new_files_added = False
    bulk_operations = []

    for filename, data in json_files.items():
        if filename not in processed_files and data['bookingReference'] not in existing_refs:
            data['filename'] = filename
            bulk_operations.append(InsertOne(data))
            processed_files.add(filename)
            new_files_added = True

    if bulk_operations:
        collection.bulk_write(bulk_operations)
    
    save_processed_files(processed_files)
    return new_files_added

def save_to_mongodb(json_data):
    """
    Save JSON data to MongoDB.
    
    Args:
    json_data (dict): The JSON data to be saved.
    
    Returns:
    ObjectId: The ID of the inserted document.
    """
    result = collection.insert_one(json_data)
    return result.inserted_id

def update_mongodb(doc_id, updated_data):
    """
    Update an existing document in MongoDB.
    
    Args:
    doc_id (ObjectId): The ID of the document to update.
    updated_data (dict): The new data to update the document with.
    """
    collection.update_one({'_id': ObjectId(doc_id)}, {'$set': updated_data})

def create_input_fields(data, prefix=''):
    """
    Recursively create input fields for nested dictionaries and lists.
    
    Args:
    data (dict or list): The data structure to create input fields for.
    prefix (str): A prefix for the field names in nested structures.
    
    Returns:
    dict or list: A structure mirroring the input, but with Streamlit input widgets.
    """
    updated_data = {}
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{prefix}{key}"
            if isinstance(value, dict):
                updated_data[key] = create_input_fields(value, f"{full_key}.")
            elif isinstance(value, list):
                updated_data[key] = create_list_input_fields(value, full_key)
            else:
                updated_data[key] = st.text_input(full_key, str(value))
    elif isinstance(data, list):
        return create_list_input_fields(data, prefix)
    else:
        return st.text_input(prefix, str(data))
    return updated_data

def create_list_input_fields(data_list, prefix):
    """
    Create input fields for list items.
    
    Args:
    data_list (list): The list to create input fields for.
    prefix (str): A prefix for the field names.
    
    Returns:
    list: A list of Streamlit input widgets or nested structures.
    """
    updated_list = []
    for i, item in enumerate(data_list):
        if isinstance(item, dict):
            with st.expander(f"{prefix} Item {i+1}"):
                updated_item = create_input_fields(item, f"{prefix}.{i}.")
        else:
            updated_item = st.text_input(f"{prefix}.{i}", str(item))
        updated_list.append(updated_item)
    return updated_list

def main():
    st.markdown(get_custom_font_css(), unsafe_allow_html=True)
    
    st.title("Shipping Instruction (SI) Editor")

    # Load JSON files from the 'si' directory
    json_files = load_json_files('./dataset/si/')

    # Save new JSON data to MongoDB
    new_files_added = save_new_documents(json_files)
    if new_files_added:
        st.success("New SI documents have been added to the database.")

    # Fetch only the booking references from MongoDB
    documents = collection.find(
        filter={},
        projection={'bookingReference': 1},
        sort=[('bookingReference', pymongo.ASCENDING)]
    )

    booking_references = [doc['bookingReference'] for doc in documents]

    # Create a dropdown to select a booking reference
    selected_ref = st.selectbox(
        "Select Booking Reference",
        options=booking_references
    )

    if selected_ref:
        # Fetch the selected document from MongoDB
        selected_doc = collection.find_one({'bookingReference': selected_ref})

        if selected_doc:
            st.write("---")
            # Create a 4-column layout
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.subheader("Voyage & Route Details")
                voyage_details = create_input_fields(selected_doc.get('voyageDetails', {}), 'Voyage: ')
                route_details = create_input_fields(selected_doc.get('routeDetails', {}), 'Route: ')
                
                st.subheader("Payment & Documentation")
                payment_details = create_input_fields(selected_doc.get('paymentDetails', {}), 'Payment: ')
                doc_details = create_input_fields(selected_doc.get('documentationDetails', {}), 'Document: ')

            with col2:
                st.subheader("Party Information")
                party_details = {}
                for party_type in ['shipper', 'consignee', 'notifyParty']:
                    party_info = selected_doc.get('partyDetails', {}).get(party_type, {})
                    st.write(f"**{party_type.capitalize()}**")
                    party_details[party_type] = {
                        'name': st.text_input(f"{party_type.capitalize()} Name", party_info.get('name', '')),
                        'address': st.text_area(f"{party_type.capitalize()} Address", party_info.get('address', '')),
                        'telephone': st.text_input(f"{party_type.capitalize()} Telephone", party_info.get('telephone', ''))
                    }

            with col3:
                st.subheader("Shipping Details")
                shipping_term = st.text_input("Shipping Terms (e.g., DOOR, CY, CFS)", selected_doc.get('shippingTerm', ''))
                hs_code = st.text_input("HS Code (Harmonized System)", selected_doc.get('hsCode', ''))
                commodity_description = st.text_area("Commodity Description", selected_doc.get('commodityDescription', ''))
                
                st.subheader("Container Information")
                containers = []
                for i, container in enumerate(selected_doc.get('containers', [])):
                    with st.expander(f"Container {i+1}"):
                        containers.append({
                            'containerNumber': st.text_input(f"Container Number {i+1}", container.get('containerNumber', '')),
                            'sealNumber': st.text_input(f"Seal Number {i+1}", container.get('sealNumber', '')),
                            'containerType': st.text_input(f"Container Type {i+1}", container.get('containerType', '')),
                            'packageType': st.text_input(f"Package Type {i+1}", container.get('packageType', '')),
                            'numberOfPackages': st.number_input(f"Number of Packages {i+1}", value=int(container.get('numberOfPackages', 0))),
                            'grossWeight': st.number_input(f"Gross Weight (kg) {i+1}", value=float(container.get('grossWeight', 0.0))),
                            'measurement': st.number_input(f"Measurement (cbm) {i+1}", value=float(container.get('measurement', 0.0))),
                            'cargoDescription': st.text_area(f"Cargo Description {i+1}", container.get('cargoDescription', '')),
                            'marksAndNumbers': st.text_area(f"Marks and Numbers {i+1}", container.get('marksAndNumbers', ''))
                        })
                
                st.subheader("Total Shipment Summary")
                total_shipment = create_input_fields(selected_doc.get('totalShipment', {}), 'Total: ')

            with col4:
                st.subheader("Additional Information")
                additional_info = create_input_fields(selected_doc.get('additionalInformation', {}), 'Additional: ')

            # Special Cargo Information section
            st.write("---")
            st.subheader("Special Cargo Information")

            # Out of Gauge Dimensions
            oog = selected_doc.get('outOfGaugeDimensions')
            if oog:
                st.write("Out of Gauge Dimensions:")
                oog_updated = {}
                for key in ['length', 'width', 'height', 'overWidth', 'overHeight']:
                    value = oog.get(key, '')
                    if value == 'In-Gauge':
                        oog_updated[key] = st.text_input(f"OOG {key.capitalize()} (mm)", value=value)
                    else:
                        try:
                            numeric_value = float(value) if value else 0
                            oog_updated[key] = st.number_input(f"OOG {key.capitalize()} (mm)", value=numeric_value)
                        except ValueError:
                            oog_updated[key] = st.text_input(f"OOG {key.capitalize()} (mm)", value=value)

            # Dangerous Goods
            dg = selected_doc.get('dangerousGoods')
            if dg:
                st.write("Dangerous Goods:")
                dg_updated = {}
                dg_updated['containerNumber'] = st.text_input("DG Container Number", value=dg.get('containerNumber', ''))
                dg_updated['unClass'] = st.text_input("DG UN Class", value=dg.get('unClass', ''))
                dg_updated['unCode'] = st.text_input("DG UN Code", value=dg.get('unCode', ''))
                dg_updated['hsCode'] = st.text_input("DG HS Code", value=dg.get('hsCode', ''))
                dg_updated['flashPoint'] = st.text_input("DG Flash Point", value=dg.get('flashPoint', ''))
                dg_updated['additionalInfo'] = st.text_area("DG Additional Info", value=dg.get('additionalInfo', ''))

            # Reefer Settings
            rs = selected_doc.get('reeferSettings')
            if rs:
                st.write("Reefer Settings:")
                rs_updated = {}
                rs_updated['containerNumber'] = st.text_input("Reefer Container Number", value=rs.get('containerNumber', ''))
                rs_updated['temperature'] = st.text_input("Reefer Temperature", value=rs.get('temperature', ''))
                rs_updated['minTemperature'] = st.text_input("Reefer Min Temperature", value=rs.get('minTemperature', ''))
                rs_updated['maxTemperature'] = st.text_input("Reefer Max Temperature", value=rs.get('maxTemperature', ''))
                rs_updated['ventilation'] = st.text_input("Reefer Ventilation", value=rs.get('ventilation', ''))
                rs_updated['humidity'] = st.text_input("Reefer Humidity", value=rs.get('humidity', ''))

            # Update button to save changes
            if st.button("Update Shipping Instruction"):
                # Collect all updated data
                updated_data = {
                    'voyageDetails': voyage_details,
                    'routeDetails': route_details,
                    'paymentDetails': payment_details,
                    'documentationDetails': doc_details,
                    'partyDetails': party_details,
                    'shippingTerm': shipping_term,
                    'hsCode': hs_code,
                    'commodityDescription': commodity_description,
                    'containers': containers,
                    'totalShipment': total_shipment,
                    'additionalInformation': additional_info,
                }
                
                # Add special cargo information if present
                if oog:
                    updated_data['outOfGaugeDimensions'] = oog_updated
                if dg:
                    updated_data['dangerousGoods'] = dg_updated
                if rs:
                    updated_data['reeferSettings'] = rs_updated

                # Update the document in MongoDB
                update_mongodb(selected_doc['_id'], updated_data)
                st.success("Shipping Instruction updated successfully!")

if __name__ == "__main__":
    main()