from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Set up MongoDB connection using environment variables
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")
COLLECTION_NAME = "si"

# Create MongoDB client and connect to the specific database and collection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
si_collection = db[COLLECTION_NAME]

# Create text index if it doesn't exist
if "text_index" not in si_collection.index_information():
    si_collection.create_index([("$**", "text")], name="text_index")

def search_shipping_instructions(query):
    regex_query = re.compile(query, re.IGNORECASE)
    
    # 정규식 검색 (모든 최상위 필드에 대해 검색)
    regex_results = si_collection.find(
        {"$or": [
            {"bookingReference": {"$regex": regex_query}},
            {"partyDetails.shipper.name": {"$regex": regex_query}},
            {"partyDetails.consignee.name": {"$regex": regex_query}},
            {"partyDetails.notifyParty.name": {"$regex": regex_query}},
            {"cargoDetails.cargoDescription": {"$regex": regex_query}},
            {"containerDetails.containerNumber": {"$regex": regex_query}},
            {"portOfLoading.name": {"$regex": regex_query}},
            {"portOfDischarge.name": {"$regex": regex_query}},
            {"vesselDetails.vesselName": {"$regex": regex_query}},
            {"voyageReference": {"$regex": regex_query}}
        ]},
        {"bookingReference": 1, "partyDetails.shipper.name": 1, "containerDetails": 1, "cargoDetails": 1}
    ).limit(10)
    
    # 텍스트 검색
    text_results = si_collection.find(
        {"$text": {"$search": query}},
        {"bookingReference": 1, "partyDetails.shipper.name": 1, "containerDetails": 1, "cargoDetails": 1, "score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})]).limit(10)
    
    # 결과 합치기 및 유사도 계산
    combined_results = []
    for doc in list(regex_results) + list(text_results):
        similarity = doc.get("score", 0.5)  # 정규식 결과의 경우 기본값 0.5
        combined_results.append({
            "_id": str(doc["_id"]),
            "bookingReference": doc.get("bookingReference"),
            "shipperName": doc.get("partyDetails", {}).get("shipper", {}).get("name"),
            "containerCount": len(doc.get("containerDetails", [])),
            "cargoDescription": doc.get("cargoDetails", {}).get("cargoDescription", ""),
            "similarity": similarity
        })
    
    # 중복 제거 및 유사도로 정렬
    unique_results = {doc["_id"]: doc for doc in combined_results}
    sorted_results = sorted(unique_results.values(), key=lambda x: x["similarity"], reverse=True)
    
    return sorted_results[:10]  # 최대 10개 결과 반환