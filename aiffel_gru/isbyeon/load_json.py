import os
import json
from pymongo import MongoClient, InsertOne
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up MongoDB connection using environment variables
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")

def load_json_files(directory):
    """지정된 디렉토리의 모든 JSON 파일을 로드하여 리스트에 저장합니다."""
    json_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                try:
                    data = json.load(f)
                    json_data.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {filename}: {e}")
    return json_data


def insert_json_to_mongodb(directory: str) -> None:

    all_data = load_json_files(directory)  # JSON 파일 로드 함수 가정

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]  # 데이터베이스 이름 변경
    collection = db[directory]  # 컬렉션 이름 변경

    # bulk_write를 사용하여 데이터 삽입
    requests = [InsertOne(data) for data in all_data]
    result = collection.bulk_write(requests)

    # 결과 확인
    if result.bulk_api_result['nInserted'] == len(all_data):
        print("Data inserted successfully")
    else:
        print("Error inserting data")


insert_json_to_mongodb('bkg')
