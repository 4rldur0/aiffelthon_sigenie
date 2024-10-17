import os
import json
import argparse
from pymongo import MongoClient, InsertOne
from bson import ObjectId
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up MongoDB connection using environment variables
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")

# Argument parser setup
parser = argparse.ArgumentParser(description='Upload JSON files from a folder to MongoDB.')
parser.add_argument('folder', type=str, help='The folder path containing JSON files')
args = parser.parse_args()

# Get folder name from the provided path to use as collection name
folder_name = os.path.basename(args.folder.rstrip('/'))
COLLECTION_NAME = folder_name

# Create MongoDB client and connect to the specific database and collection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def load_json_files(directory):
    """Load all JSON files from the specified directory."""
    json_files = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                try:
                    json_files[filename] = json.load(file)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {filename}: {e}")
    return json_files

def insert_documents(json_files):
    """Insert all JSON documents to MongoDB without checking for duplicates."""
    bulk_operations = [InsertOne(data) for data in json_files.values()]

    if bulk_operations:
        try:
            collection.bulk_write(bulk_operations)
            print(f"{len(bulk_operations)} JSON documents have been added to the database.")
        except Exception as e:
            print(f"Error writing to MongoDB: {e}")
    else:
        print("No JSON files to add.")

def remove_duplicates():
    """Remove documents with duplicate bookingReference."""
    pipeline = [
        { "$sort": { "bookingReference": 1, "_id": 1 } },
        {
            "$group": {
                "_id": "$bookingReference",
                "dups": { "$push": "$_id" },
                "count": { "$sum": 1 }
            }
        },
        { "$match": { "count": { "$gt": 1 } } }
    ]

    duplicates = collection.aggregate(pipeline, allowDiskUse=True)

    for doc in duplicates:
        # Keep the first document, remove the rest
        doc['dups'].pop(0)
        collection.delete_many({ "_id": { "$in": doc['dups'] } })
        print(f"Removed {len(doc['dups'])} duplicate(s) for bookingReference: {doc['_id']}")

def main():
    # Load JSON files from the specified folder
    json_files = load_json_files(args.folder)

    # Insert all JSON data to MongoDB
    insert_documents(json_files)

    # Remove duplicates based on bookingReference
    remove_duplicates()

if __name__ == "__main__":
    main()
