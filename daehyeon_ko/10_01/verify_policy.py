"""
# 주요 업데이트
1. 비동기 검색 : 'aiohttp' 라이브러리를 사용해 비동기적 웹 검색을 수행
검색된 제재 리스트 정보를 'retrieve_updated_sanction_list' 메서드를 통해 확인

2. 문서 검색 및 웹 검색 통합 : RAG 모델을 통해 문서와 
웹 검색 결과를 결합해, 최신 정보를 반영한 답변을 생성
"""

# Step 0 : 필수 라이브러리 불러오기
import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict, Any
from langchain_core.output_parsers import StrOutputParser
import asyncio
from web_search import WebSearch # web_search 모듈에서 불러오기

# Step 1: 회사 정책 문서를 불러오는 함수 (PDF나 URL 지원)
def load_documents(sources: List[str]) -> List:
    """
    주어진 소스 리스트에서 문서를 불러오기
    """
    docs = []
    for source in sources:
        try:
            if source.startswith('http'):
                print(f"Loading documents from URL: {source}")
                loader = WebBaseLoader(source)
            elif source.endswith('.pdf'):
                print(f"Loading documents from PDF: {source}")
                loader = PyPDFLoader(source)
            else:
                print(f"Unsupported source type: {source}")
                continue
            docs.extend(loader.load())
        except Exception as e:
            print(f"Error loading from {source}: {e}")
    return docs

# Step 2: FAISS 벡터 스토어 생성하는 함수
def create_vectorstore(documents):
    """
    주어진 문서에서 FAISS 벡터 스토어를 생성하여 로컬에 저장
    """
    embedding_model = OpenAIEmbeddings()

    # 긴 문서를 조각내고, 효율적으로 검색할 수 있도록 설정하기
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = text_splitter.split_documents(documents)

    # FAISS 벡터 스토어 생성하기
    vectorstore = FAISS.from_documents(split_docs, embedding_model)

    # 로컬에 저장하기
    vectorstore.save_local("faiss_index")
    print("Vector store created and saved locally at 'faiss_index'.")
    return vectorstore

# Step 3: 벡터 스토어 하수 불러오기 또는 새로 생성하기
def load_vectorstore(sources: List[str]):
    """
    로컬에 저장된 벡터 스토어를 불러오거나,
    존재하지 않을 경우 새로 생성하기
    """
    # 로칼에 저징된 벡터 스토어가 있는 경우 불러오기
    if os.path.exists("faiss_index/index.faiss"):
        print("Loading existing vector store from 'faiss_index'.")
        return FAISS.load_local("faiss_index", OpenAIEmbeddings(), allow_dangerous_deserialization=True)
    # 존재하지 않을 경우 새로 벡터 스토어 생성하기
    else:
        print("Vector store not found. Loading documents and creating a new vector store.")
        documents = load_documents(sources)
        return create_vectorstore(documents)

# Step 4: RAG 모델 클래스 만들기
class RAGModel:
    def __init__(self, llm, sources: List[str], template):
        """
        RAG 모델 초기화: 벡터 스토어 및 프롬프트 템플릿 설정
        """
        self.vectorstore = load_vectorstore(sources)
        self.llm = llm
        self.prompt = PromptTemplate(template=template, input_variables=["si_data"])
        self.chain = self.prompt | self.llm | StrOutputParser()

    def retrieve_documents(self, question: str):
        """
        벡터 스토어에서 주어진 질문과 관련된 문서를 검색
        """
        retriever = self.vectorstore.as_retriever(search_kwargs={'k': 5})
        relevant_docs = retriever.get_relevant_documents(question)
        return relevant_docs

    async def retrieve_updated_sanction_list(self, si_data: dict):
        """
        SI 데이터(SHIPPER, CONSIGNEE, 등)에 연관된 제재 리스트를 
        웹 검색을 통해 업데이트된 정보로 확인
        """
        # aiohttp 세션 생성하기
        async with aiohttp.ClientSession() as session:
            web_search = WebSearch(session)
            
            # 검색어 동적으로 생성하기
            query = (
                f"Find sanction list related to {si_data['SHIPPER']}, "
                f"{si_data['CONSIGNEE']}, {si_data['NOTIFY_PARTIES']}, "
                f"{si_data['HS_CODE']}, {si_data['CARGO_ITEM']}"
            )
            
            # 포함/제외 URL 설정하기 (예시)
            """
            실시간 검색에서 포함/제외할 URL을 설정하는 것으로, 위의 RAG 생성 코드와는 다름
            """
            web_search.set_include_urls(['https://해당 주소를 포함해 주세요.com'])  # 포함 URL 설정하기 (예시)
            web_search.set_exclude_urls(['https://해당 주소는 제외해 주세요.com'])  # 제외 URL 설정하기 (예시)
            
            # 웹 검색 수행하기
            results = await web_search.search(query)
            return results

    def generate_response(self, si_data: str, retrieved_docs: list, sanction_updates: list):
        """
        검색된 문서와 웹 검색 결과를 바탕으로 응답을 생성하기
        """
        # 문서와 제재 업데이트 내용을 결합하여 컨텍스트 생성하기
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        sanction_info = "\n".join(sanction_updates)
        question_with_context = f"{si_data}\n\nRelevant Documents:\n{context}\n\nUpdated Sanction List:\n{sanction_info}"
        
        # LLM을 사용하여 응답 생성
        return self.chain.invoke({'si_data': question_with_context})

    async def invoke(self, si_data: dict):
        """
        주어진 SI 데이터에 대해 문서를 검색하고, 웹 검색을 통해 최신 제재 리스트를 확인한 후 응답을 생성하는 메인 함수
        """
        # 1. 벡터 스토어에서 관련 문서 검색하기
        retrieved_docs = self.retrieve_documents(si_data['SHIPPER'])
        
        # 2. 웹 검색을 통해 최신 제재 리스트 확인하기
        sanction_updates = await self.retrieve_updated_sanction_list(si_data)
        
        # 3. 문서와 웹 검색 결과를 바탕으로 응답 생성하기
        response = self.generate_response(si_data, retrieved_docs, sanction_updates)
        print(response)
        return response
