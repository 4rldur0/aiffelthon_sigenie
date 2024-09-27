import os
from pymongo import MongoClient
from dotenv import load_dotenv

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

def fetch_shipping_instruction(booking_reference):
    """
    Fetch the shipping instruction from MongoDB based on the booking reference.
    """
    return collection.find_one({'bookingReference': booking_reference})

# ========= 예약 번호 말고 다른 정보로도 조회할 수 있는 방법 추가하면 좋을 듯 =========
