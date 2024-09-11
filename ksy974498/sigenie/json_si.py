import os
import json
import streamlit as st
from pymongo import MongoClient, InsertOne
from bson import ObjectId
from dotenv import load_dotenv

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

# Apply custom CSS to use Avenir font
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Avenir:wght@400;700&display=swap');
    html, body, [class*="st-"] {
        font-family: 'Avenir', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

PROCESSED_FILES_JSON = 'processed_si_files.json'

def load_processed_files():
    if os.path.exists(PROCESSED_FILES_JSON):
        with open(PROCESSED_FILES_JSON, 'r') as f:
            return set(json.load(f))
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
    st.title("Shipping Instruction JSON Editor")

    # Load JSON files from the 'si' directory
    json_files = load_json_files('./si/')

    # Save new JSON data to MongoDB
    new_files_added = save_new_documents(json_files)
    if new_files_added:
        st.success("New SI documents have been added to the database.")

    # Fetch only the booking references from MongoDB
    booking_references = [doc['bookingReference'] for doc in collection.find({}, {'bookingReference': 1})]

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
                # Display and allow editing of voyage and route details
                st.subheader("Voyage & Route Details")
                voyage_details = create_input_fields(selected_doc.get('voyageDetails', {}), 'voyageDetails.')
                route_details = create_input_fields(selected_doc.get('routeDetails', {}), 'routeDetails.')
                
                # Display and allow editing of payment and documentation details
                st.subheader("Payment & Documentation")
                payment_details = create_input_fields(selected_doc.get('paymentDetails', {}), 'paymentDetails.')
                doc_details = create_input_fields(selected_doc.get('documentationDetails', {}), 'documentationDetails.')

            with col2:
                # Display and allow editing of party details
                st.subheader("Party Details")
                party_details = create_input_fields(selected_doc.get('partyDetails', {}), 'partyDetails.')

            with col3:
                # Display and allow editing of shipping information
                st.subheader("Shipping Information")
                shipping_term = st.text_input("shippingTerm", selected_doc.get('shippingTerm', ''))
                hs_code = st.text_input("hsCode", selected_doc.get('hsCode', ''))
                commodity_description = st.text_area("commodityDescription", selected_doc.get('commodityDescription', ''))
                
                # Display and allow editing of container information
                st.subheader("Containers")
                containers = create_input_fields(selected_doc.get('containers', []), 'containers')
                
                # Display and allow editing of total shipment information
                st.subheader("Total Shipment")
                total_shipment = create_input_fields(selected_doc.get('totalShipment', {}), 'totalShipment.')

            with col4:
                # Display and allow editing of additional information
                st.subheader("Additional Information")
                additional_info = create_input_fields(selected_doc.get('additionalInformation', {}), 'additionalInformation.')

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
                        oog_updated[key] = st.text_input(f"{key.capitalize()} (mm)", value=value)
                    else:
                        try:
                            numeric_value = float(value) if value else 0
                            oog_updated[key] = st.number_input(f"{key.capitalize()} (mm)", value=numeric_value)
                        except ValueError:
                            oog_updated[key] = st.text_input(f"{key.capitalize()} (mm)", value=value)

            # Dangerous Goods
            dg = selected_doc.get('dangerousGoods')
            if dg:
                st.write("Dangerous Goods:")
                dg_updated = {}
                dg_updated['containerNumber'] = st.text_input("Container Number (DG)", value=dg.get('containerNumber', ''))
                dg_updated['unClass'] = st.text_input("UN Class", value=dg.get('unClass', ''))
                dg_updated['unCode'] = st.text_input("UN Code", value=dg.get('unCode', ''))
                dg_updated['hsCode'] = st.text_input("HS Code (DG)", value=dg.get('hsCode', ''))
                dg_updated['flashPoint'] = st.text_input("Flash Point", value=dg.get('flashPoint', ''))
                dg_updated['additionalInfo'] = st.text_area("Additional Info (DG)", value=dg.get('additionalInfo', ''))

            # Reefer Settings
            rs = selected_doc.get('reeferSettings')
            if rs:
                st.write("Reefer Settings:")
                rs_updated = {}
                rs_updated['containerNumber'] = st.text_input("Container Number (Reefer)", value=rs.get('containerNumber', ''))
                rs_updated['temperature'] = st.text_input("Temperature", value=rs.get('temperature', ''))
                rs_updated['minTemperature'] = st.text_input("Min Temperature", value=rs.get('minTemperature', ''))
                rs_updated['maxTemperature'] = st.text_input("Max Temperature", value=rs.get('maxTemperature', ''))
                rs_updated['ventilation'] = st.text_input("Ventilation", value=rs.get('ventilation', ''))
                rs_updated['humidity'] = st.text_input("Humidity", value=rs.get('humidity', ''))

            # Update button to save changes
            if st.button("Update"):
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
                st.success("Document updated successfully!")

if __name__ == "__main__":
    main()