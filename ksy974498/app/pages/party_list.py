import streamlit as st
from pymongo import MongoClient
import pandas as pd

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection setup
def get_mongodb_client():
    client = MongoClient(os.getenv('MONGODB_URI'))
    return client

# Fetch all documents from the collection and extract unique party details based on 'name'
def fetch_unique_parties(client):
    MONGODB_DB_NAME = 'ContainerGenie'  # Your database name
    MONGODB_COLLECTION_NAME = 'si'      # Your collection name
    
    db = client[MONGODB_DB_NAME]
    collection = db[MONGODB_COLLECTION_NAME]
    
    # Fetch all documents
    documents = collection.find()
    
    # Extract all party details (Shipper, Consignee, Notify Party) into a list
    party_list = []
    for doc in documents:
        party_details = doc.get("partyDetails", {})
        if party_details:
            # Extract each party and append to the list
            shipper = party_details.get("shipper", {})
            consignee = party_details.get("consignee", {})
            notify_party = party_details.get("notifyParty", {})
            
            if shipper:
                party_list.append(shipper)
            if consignee:
                party_list.append(consignee)
            if notify_party:
                party_list.append(notify_party)

    # Convert the list of parties into a DataFrame
    df = pd.DataFrame(party_list)
    
    # Drop duplicate parties based on the 'name' field
    unique_parties_df = df.drop_duplicates(subset=['name'])
    
    return unique_parties_df

# Streamlit app
def main():
    st.title("Party Details Viewer")
    
    # MongoDB client
    client = get_mongodb_client()
    
    # Fetch unique party details
    df = fetch_unique_parties(client)
    
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