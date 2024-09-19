import streamlit as st
from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection setup
def get_mongodb_client():
    MONGODB_URI = 'mongodb+srv://ksy974498:HOm7No7wIQ2QGnoP@cluster0.lu3l6.mongodb.net/test?retryWrites=true&w=majority'
    client = MongoClient(MONGODB_URI)
    return client

# Fetch all documents from the collection and extract party details
def fetch_all_party_details(client):
    MONGODB_DB_NAME = 'ContainerGenie'  # Your database name
    MONGODB_COLLECTION_NAME = 'si'      # Your collection name
    
    db = client[MONGODB_DB_NAME]
    collection = db[MONGODB_COLLECTION_NAME]
    
    # Fetch all documents
    documents = collection.find()
    
    # Extract and combine party details (Shipper, Consignee, Notify Party)
    data = []
    for doc in documents:
        party_details = doc.get("partyDetails", {})
        if party_details:
            # Extract shipper, consignee, and notify party details
            shipper = party_details.get("shipper", {})
            consignee = party_details.get("consignee", {})
            notify_party = party_details.get("notifyParty", {})
            
            # Append details to the data list with a category label
            if shipper:
                data.append({
                    "Type": "Shipper",
                    "Name": shipper.get("name", ""),
                    "Address": shipper.get("address", ""),
                    "Telephone": shipper.get("telephone", ""),
                    "Email/Fax": shipper.get("email", "")
                })
            if consignee:
                data.append({
                    "Type": "Consignee",
                    "Name": consignee.get("name", ""),
                    "Address": consignee.get("address", ""),
                    "Telephone": consignee.get("telephone", ""),
                    "Email/Fax": consignee.get("fax", ""),
                    "President": consignee.get("president", ""),
                    "Tax ID": consignee.get("taxId", "")
                })
            if notify_party:
                data.append({
                    "Type": "Notify Party",
                    "Name": notify_party.get("name", ""),
                    "Address": notify_party.get("address", ""),
                    "Telephone": notify_party.get("telephone", ""),
                    "Email/Fax": notify_party.get("fax", ""),
                    "President": notify_party.get("president", ""),
                    "Tax ID": notify_party.get("taxId", "")
                })
    
    return pd.DataFrame(data)

# Streamlit app
def main():
    st.title("Party Details Viewer")
    
    # MongoDB client
    client = get_mongodb_client()
    
    # Fetch all party details
    df = fetch_all_party_details(client)
    
    # Search box for filtering the table
    search_query = st.text_input("Search by name, address, or telephone:")
    
    if search_query:
        # Filter the dataframe based on the search query
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    else:
        filtered_df = df
    
    # Display the filtered or full table
    st.dataframe(filtered_df)

if __name__ == "__main__":
    main()
