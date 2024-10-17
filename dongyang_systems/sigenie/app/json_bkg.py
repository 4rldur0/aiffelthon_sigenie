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
COLLECTION_NAME = "bkg"

# Create MongoDB client and connect to the specific database and collection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

PROCESSED_FILES_JSON = './dataset/processed_bkg_files.json'

def load_processed_files():
    if os.path.exists(PROCESSED_FILES_JSON):
        with open(PROCESSED_FILES_JSON, 'r') as f:
            return set(json.load(f))
    return set()

def save_processed_files(processed_files):
    with open(PROCESSED_FILES_JSON, 'w') as f:
        json.dump(list(processed_files), f)

def load_json_files(directory):
    json_files = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                json_files[filename] = json.load(file)
    return json_files

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

def update_mongodb(doc_id, updated_data):
    collection.update_one({'_id': ObjectId(doc_id)}, {'$set': updated_data})

def create_input_fields(data, prefix=''):
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
    st.title("Booking (BKG) Editor")

    # Load JSON files from the 'bkg' directory
    json_files = load_json_files('./dataset/bkg/')

    # Save new JSON data to MongoDB
    new_files_added = save_new_documents(json_files)
    if new_files_added:
        st.success("New BKG documents have been added to the database.")

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
            
            # 상단 정보
            st.subheader("Basic Booking Information")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Booking Reference Number", selected_doc.get('bookingReference', ''))
                st.text_input("Customer Full Name", selected_doc.get('customerName', ''))
                st.text_input("Shipper Full Name", selected_doc.get('shipperName', ''))
            with col2:
                st.text_input("Invoice Recipient", selected_doc.get('invoiceReceiver', ''))
                st.text_input("Shipping Terms (e.g., DOOR, CY, CFS)", selected_doc.get('shippingTerm', ''))

            st.write("---")

            # 중앙 정보
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.subheader("Voyage Information")
                voyage_details = create_input_fields(selected_doc.get('voyageDetails', {}), 'Voyage: ')
                
                st.subheader("Route Information")
                route_details = create_input_fields(selected_doc.get('routeDetails', {}), 'Route: ')
                
                st.subheader("Schedule Information")
                schedule_details = create_input_fields(selected_doc.get('scheduleDetails', {}), 'Schedule: ')

            with col_right:
                st.subheader("Cargo Information")
                cargo_details = create_input_fields(selected_doc.get('cargoDetails', {}), 'Cargo: ')
                
                st.subheader("Container Information")
                container_details = create_input_fields(selected_doc.get('containerDetails', {}), 'Container: ')
                
                st.subheader("Empty Container Pickup Location")
                pickup_location = create_input_fields(selected_doc.get('emptyContainerPickupLocation', {}), 'Pickup: ')

            st.write("---")

            # 하단 정보
            st.subheader("Additional Remarks")
            remarks = st.text_area("Special Instructions or Notes", selected_doc.get('remarks', ''))

            # Update button
            if st.button("Update"):
                updated_data = {
                    'bookingReference': selected_doc['bookingReference'],
                    'customerName': selected_doc['customerName'],
                    'shipperName': selected_doc['shipperName'],
                    'invoiceReceiver': selected_doc['invoiceReceiver'],
                    'shippingTerm': selected_doc['shippingTerm'],
                    'voyageDetails': voyage_details,
                    'routeDetails': route_details,
                    'scheduleDetails': schedule_details,
                    'cargoDetails': cargo_details,
                    'containerDetails': container_details,
                    'emptyContainerPickupLocation': pickup_location,
                    'remarks': remarks
                }
                update_mongodb(selected_doc['_id'], updated_data)
                st.success("Document updated successfully!")

if __name__ == "__main__":
    main()
