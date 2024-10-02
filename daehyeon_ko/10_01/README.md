### 코드 개요
* `verify_policy.py` : 문서 검색, FAISS 벡터 저장소 관리, 회사 정책 및 제재 리스트를 기반으로 응답을 생성
* `web_search.py` : Tavily API를 활용한 실시간 웹 검색, HTML 및 PDF 파일에서 텍스트 추출, URL 필터링 기능 제공

### 기능 설명
* `verify_policy.py`
    * 문서 로딩 : PDF 또는 URL 기반 문서를 로드하고, **RecursiveCharacterTextSplitter**를 사용하여 작은 단위로 나누어 검색 가능하게 만듦
    * FAISS 벡터 스토어 : 로드된 문서로부터 FAISS 벡터 스토어를 생성하여, 관련 섹션을 빠르게 검색 가능
    * 제재 리스트 검색 : `web_search.py`를 통해 최신 제재 리스트를 실시간으로 검색
    * 응답 생성 : 벡터 검색 결과와 실시간 검색 결과를 결합하여 제공된 SI 데이터를 기반으로 최종 응답을 생성
 
```
rag_model = RAGModel(llm=your_llm_instance, sources=sources, template=your_prompt_template)
await rag_model.invoke(si_data)
```

* `web_search.py`
    * Tavily API 통합 : **Tavily API**를 사용하여 실시간으로 웹 검색을 수행. API 요청에는 검색어, 포함할 URL, 제외할 URL 등의 필터링 규칙이 포함됨.
    * 비동기 HTTP 요청 : **aiohttp**를 사용하여 비동기 방식으로 HTTP 요청을 수행하여 검색 성능을 최적화
    * URL 필터링 : **포함/제외 URL** 목록을 기반으로 검색 결과를 필터링하여 적절한 결과만을 처리
    * HTML 및 PDF 파싱 : **BeautifulSoup**을 사용하여 HTML 페이지에서 텍스트를 추출하고, **PyPDF2**를 사용하여 PDF 문서에서 텍스트를 추출
 
### 필요 라이브러리 및 Tavily API 필요
```
pip install aiohttp python-dotenv PyPDF2 beautifulsoup4
```
