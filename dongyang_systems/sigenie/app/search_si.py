import os
import re
import json
import hashlib
import asyncio
import streamlit as st
import pymongo
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
from datetime import datetime, timezone
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from utils.helpers import get_custom_font_css
import numpy as np
from tqdm import tqdm

# Load environment variables and set up constants
load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")
COLLECTION_NAME = "si"
FAISS_INDEX_FOLDER = "./vector/si_faiss_index"
LAST_UPDATE_FILE = f"{FAISS_INDEX_FOLDER}/last_update.txt"

# Ensure necessary directories exist
os.makedirs(FAISS_INDEX_FOLDER, exist_ok=True)

# Set up MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Set up OpenAI API
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings()

# Initialize embedding cache
embedding_cache = {}

# Helper functions for FAISS index and last update time
def save_faiss_index(vectorstore):
    vectorstore.save_local(FAISS_INDEX_FOLDER)

def load_faiss_index():
    try:
        if os.path.exists(FAISS_INDEX_FOLDER):
            index_file = os.path.join(FAISS_INDEX_FOLDER, "index.faiss")
            if os.path.exists(index_file):
                return FAISS.load_local(FAISS_INDEX_FOLDER, embeddings, allow_dangerous_deserialization=True)
            else:
                st.warning(f"FAISS index file not found in {FAISS_INDEX_FOLDER}. A new one will be created.")
        else:
            st.warning(f"FAISS index folder {FAISS_INDEX_FOLDER} not found. A new one will be created.")
        return None
    except Exception as e:
        st.error(f"Error loading FAISS index: {str(e)}")
        return None

def save_last_update(last_update):
    with open(LAST_UPDATE_FILE, "w") as f:
        f.write(last_update.isoformat())

def load_last_update():
    if os.path.exists(LAST_UPDATE_FILE):
        with open(LAST_UPDATE_FILE, "r") as f:
            try:
                return datetime.fromisoformat(f.read().strip())
            except ValueError:
                st.warning("Invalid date in last_update file. Using minimum date.")
    return datetime.min.replace(tzinfo=timezone.utc)

# Caching function for embeddings
def get_cached_embedding(text):
    text_hash = hashlib.md5(text.encode()).hexdigest()
    if text_hash in embedding_cache:
        return embedding_cache[text_hash]
    embedding = embeddings.embed_query(text)
    embedding_cache[text_hash] = embedding
    return embedding

# MongoDB and Vector DB update functions
def check_mongodb_update():
    last_update = load_last_update()
    latest_doc = collection.find_one(sort=[('_id', pymongo.DESCENDING)])
    
    if latest_doc and latest_doc['_id'].generation_time > last_update:
        new_last_update = latest_doc['_id'].generation_time
        save_last_update(new_last_update)
        return True
    return False

async def update_faiss_index(create_new=False):
    last_update = load_last_update()
    
    if create_new:
        updated_docs = list(collection.find())
    else:
        updated_docs = list(collection.find({'_id': {'$gt': ObjectId.from_datetime(last_update)}}))
    
    if not updated_docs:
        st.info("No new updates found in MongoDB.")
        return st.session_state.get('vectorstore')

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    
    # Batch processing
    batch_size = 100
    all_texts = []
    all_metadatas = []
    
    for i in tqdm(range(0, len(updated_docs), batch_size)):
        batch = updated_docs[i:i+batch_size]
        texts = text_splitter.split_documents([Document(page_content=json.dumps(doc, default=str), metadata={"id": str(doc["_id"])}) for doc in batch])
        all_texts.extend([text.page_content for text in texts])
        all_metadatas.extend([text.metadata for text in texts])

    async def get_embeddings_batch(texts):
        return await asyncio.gather(*[asyncio.to_thread(get_cached_embedding, text) for text in texts])

    # Parallel processing
    embeddings_list = []
    for i in tqdm(range(0, len(all_texts), batch_size)):
        batch_texts = all_texts[i:i+batch_size]
        batch_embeddings = await get_embeddings_batch(batch_texts)
        embeddings_list.extend(batch_embeddings)

    # Convert to numpy array for efficient operations
    embeddings_array = np.array(embeddings_list)

    # Combine texts and embeddings into the format expected by FAISS
    text_embeddings = list(zip(all_texts, embeddings_array))

    if create_new or 'vectorstore' not in st.session_state or st.session_state.vectorstore is None:
        vectorstore = FAISS.from_embeddings(text_embeddings, embeddings, metadatas=all_metadatas)
    else:
        vectorstore = st.session_state.vectorstore
        vectorstore.add_embeddings(text_embeddings, metadatas=all_metadatas)
    
    save_faiss_index(vectorstore)
    if updated_docs:
        new_last_update = max(doc['_id'].generation_time for doc in updated_docs)
        save_last_update(new_last_update)
    st.success(f"Vector DB {'created' if create_new else 'updated'} with {len(updated_docs)} documents.")
    return vectorstore

def initialize_vector_db():
    if 'vectorstore' not in st.session_state or st.session_state.vectorstore is None:
        st.session_state.vectorstore = load_faiss_index()
        if st.session_state.vectorstore is None:
            st.warning("Creating new Vector DB from scratch...")
            st.session_state.vectorstore = asyncio.run(update_faiss_index(create_new=True))
    
    if check_mongodb_update():
        st.warning("MongoDB has been updated. Updating Vector DB...")
        st.session_state.vectorstore = asyncio.run(update_faiss_index(create_new=False))

# JSON encoder to handle ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# Main application function
def main():
    st.markdown(get_custom_font_css(), unsafe_allow_html=True)
    st.title("Vector Search in MongoDB")

    initialize_vector_db()

    search_value = st.text_area("Enter search term", height=100)

    st.markdown("""
        **Similarity Threshold**: This slider controls how similar a document must be to the search query to be included in the results. 
        A lower value will return more results, allowing documents that are less similar to the query.
        A higher value will return fewer results, requiring documents to be more similar to the query.
        The threshold ranges from 0 (include all results) to 1 (include only the most similar results).
    """)
    similarity_threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.5, 0.01)

    if st.button("Search"):
        if search_value and st.session_state.vectorstore:
            try:
                vector_results = st.session_state.vectorstore.similarity_search_with_score(search_value, k=50)
                keyword_pattern = re.compile(re.escape(search_value), re.IGNORECASE)
                exact_match_fields = ['bookingReference']
                exact_match_query = {field: search_value for field in exact_match_fields}
                
                st.session_state.results = []
                
                exact_matches = list(collection.find(exact_match_query))
                for mongo_doc in exact_matches:
                    mongo_doc['vector_score'] = 0
                    mongo_doc['keyword_match'] = True
                    mongo_doc['hybrid_score'] = 3
                    mongo_doc['match_type'] = 'Exact'
                    st.session_state.results.append(mongo_doc)
                
                for doc, score in vector_results:
                    mongo_doc = collection.find_one({"_id": ObjectId(doc.metadata["id"])})
                    if mongo_doc and mongo_doc not in exact_matches:
                        if score <= (1 - similarity_threshold):
                            keyword_match = any(keyword_pattern.search(str(value)) for value in mongo_doc.values())
                            
                            mongo_doc['vector_score'] = float(score)
                            mongo_doc['keyword_match'] = keyword_match
                            mongo_doc['hybrid_score'] = 1 / (1 + score) * (2 if keyword_match else 1)
                            mongo_doc['match_type'] = 'Vector'
                            
                            st.session_state.results.append(mongo_doc)
                
                st.session_state.results.sort(key=lambda x: x['hybrid_score'], reverse=True)
                
                if not st.session_state.results:
                    st.warning("No matching data found.")
            except Exception as e:
                st.error(f"An error occurred during the search: {str(e)}")
        else:
            st.warning("Please enter a search term.")

    if 'results' in st.session_state and st.session_state.results:
        st.subheader("Search Results (sorted by relevance):")
        
        st.markdown("""
        **Scoring Metrics Explanation**:
        - **Hybrid Score**: A combined score that balances vector similarity and keyword matching. Higher is better.
          Formula: `1 / (1 + vector_score) * (2 if keyword_match else 1)`
        - **Vector Score**: Measures how semantically similar the document is to the query. Lower is better (closer to 0 means more similar).
          Range: 0 to 1, where 0 is most similar.
        - **Keyword Match**: Indicates whether the exact search term was found in the document (True/False).
          True if any field in the document contains the exact search term.

        The Hybrid Score combines vector similarity with keyword matching:
        - The `1 / (1 + vector_score)` part ensures that lower vector scores (more similar) result in higher hybrid scores.
        - The `* (2 if keyword_match else 1)` part doubles the score if there's an exact keyword match.
        """)
        
        df = pd.DataFrame(st.session_state.results)
        columns = ['hybrid_score', 'vector_score', 'keyword_match'] + [col for col in df.columns if col not in ['hybrid_score', 'vector_score', 'keyword_match']]
        df = df[columns]
        
        for col in df.columns:
            df[col] = df[col].astype(str)
        
        st.dataframe(df, height=300)
        
        selected_index = st.selectbox("Select a row to view details:", 
                                      options=range(len(df)),
                                      format_func=lambda i: f"Row {i+1}: Score {df.iloc[i]['hybrid_score']} - {df.iloc[i].get('bookingReference', 'N/A')}")
        
        if st.button("View Details"):
            selected_item = st.session_state.results[selected_index]
            for field in ['hybrid_score', 'vector_score', 'keyword_match']:
                selected_item.pop(field, None)
            
            json_data = json.dumps(selected_item, ensure_ascii=False, indent=2, cls=JSONEncoder)
            
            st.subheader("Selected Item Details:")
            st.json(json_data)
    elif search_value:
        st.warning("No matching data found.")

if __name__ == "__main__":
    main()
