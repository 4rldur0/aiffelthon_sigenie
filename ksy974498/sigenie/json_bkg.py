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
COLLECTION_NAME = "bkg"

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

PROCESSED_FILES_JSON = 'processed_bkg_files.json'

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
    st.title("Booking JSON Editor")

    # Load JSON files from the 'bkg' directory
    json_files = load_json_files('./bkg/')

    # Save new JSON data to MongoDB
    new_files_added = save_new_documents(json_files)
    if new_files_added:
        st.success("New BKG documents have been added to the database.")

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
            # Create input fields for all sections of the booking document
            updated_data = create_input_fields(selected_doc)

            # Update button to save changes
            if st.button("Update"):
                # Update the document in MongoDB
                update_mongodb(selected_doc['_id'], updated_data)
                st.success("Document updated successfully!")

if __name__ == "__main__":
    main()