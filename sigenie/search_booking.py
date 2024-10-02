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
COLLECTION_NAME = "bkg"

# Create MongoDB client and connect to the specific database and collection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
booking_collection = db[COLLECTION_NAME]

# Create text index if it doesn't exist
if "text_index" not in booking_collection.index_information():
    booking_collection.create_index([("$**", "text")], name="text_index")

def search_booking(query):
    print(f"Searching for: {query}")  # 디버깅을 위한 print 문
    regex_query = re.compile(query, re.IGNORECASE)
    
    # 정규식 검색 (모든 최상위 필드에 대해 검색)
    regex_results = booking_collection.find(
        {"$or": [
            {"bookingReference": {"$regex": regex_query}},
            {"customerName": {"$regex": regex_query}},
            {"cargoDetails.cargoDescription": {"$regex": regex_query}},
            {"cargoDetails.chapterDescription": {"$regex": regex_query}},
            {"containerDetails.containerNumber": {"$regex": regex_query}},
            {"portOfLoading.name": {"$regex": regex_query}},
            {"portOfDischarge.name": {"$regex": regex_query}},
            {"vesselDetails.vesselName": {"$regex": regex_query}},
            {"voyageReference": {"$regex": regex_query}}
        ]},
        {"bookingReference": 1, "customerName": 1, "containerDetails": 1, "cargoDetails": 1}
    ).limit(10)
    
    # 텍스트 검색
    text_results = booking_collection.find(
        {"$text": {"$search": query}},
        {"bookingReference": 1, "customerName": 1, "containerDetails": 1, "cargoDetails": 1, "score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})]).limit(10)
    
    # 결과 합치기 및 유사도 계산
    combined_results = []
    for doc in list(regex_results) + list(text_results):
        similarity = doc.get("score", 0.5)  # 정규식 결과의 경우 기본값 0.5
        container_details = doc.get("containerDetails", [])
        
        if isinstance(container_details, list):
            container_count = sum(container.get("quantity", 0) if isinstance(container, dict) else 0 for container in container_details)
        elif isinstance(container_details, dict):
            container_count = container_details.get("quantity", 0)
        else:
            container_count = 0
        
        combined_results.append({
            "_id": str(doc["_id"]),
            "bookingReference": doc.get("bookingReference"),
            "customerName": doc.get("customerName"),
            "containerCount": container_count,
            "chapterDescription": doc.get("cargoDetails", {}).get("chapterDescription", ""),
            "similarity": similarity
        })
    
    # 중복 제거 및 유사도로 정렬
    unique_results = {doc["_id"]: doc for doc in combined_results}
    sorted_results = sorted(unique_results.values(), key=lambda x: x["similarity"], reverse=True)
    
    print(f"Search results: {sorted_results}")  # 디버깅을 위한 print 문
    return sorted_results[:10]  # 최대 10개 결과 반환