# 라이브러리 불러오기
import aiohttp
import os
from typing import List, Optional
from dotenv import load_dotenv  # dotenv를 통해 환경 변수를 로드

# .env 파일에서 API 토큰 로드
load_dotenv()

class WebSearch:
    """
    Tavily 검색 API를 사용하여 웹 검색을 수행하고, 
    포함 및 제외 URL 조건에 따라 결과를 필터링하는 클래
    """
    
    def __init__(self, session: aiohttp.ClientSession):
        """
        WebSearch 클래스 초기화
        :param session: aiohttp.ClientSession 객체 (비동기 요청 처리)
        """
        self.session = session
        self.include_urls = []
        self.exclude_urls = []
        self.api_token = os.getenv('TAVILY_API_TOKEN')  # .env에서 API 토큰 가져오기

    def set_include_urls(self, include_urls: List[str]):
        """
        포함할 URL 리스트 설정
        :param include_urls: 검색 결과에 반드시 포함할 URL 리스트
        """
        self.include_urls = include_urls

    def set_exclude_urls(self, exclude_urls: List[str]):
        """
        제외할 URL 리스트 설정
        :param exclude_urls: 검색 결과에서 제외할 URL 리스트
        """
        self.exclude_urls = exclude_urls

    async def search(self, query: str, num_results: int = 5) -> List[str]:
        """
        Tavily API를 사용해 주어진 쿼리로 검색을 수행하고, 검색 결과를 반환
        :param query: 검색할 쿼리 (문자열)
        :param num_results: 가져올 검색 결과의 개수 (기본값: 5)
        :return: 검색된 결과의 리스트 (URL 또는 텍스트)
        """
        print(f"Performing web search for query: {query}")
        
        # Tavily API를 사용하여 검색 수행 (실제 API URL 및 토큰 사용)
        search_results = []
        tavily_api_url = "https://api.tavily.com/search"
        
        # API에 필요한 파라미터 설정
        params = {
            "q": query,  # 검색어
            "include_urls": ",".join(self.include_urls),  # 포함할 URL 리스트
            "exclude_urls": ",".join(self.exclude_urls),  # 제외할 URL 리스트
            "num_results": num_results  # 결과의 개수
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_token}"  # API 토큰 헤더에 추가
        }

        # 비동기 API 호출
        async with self.session.get(tavily_api_url, params=params, headers=headers) as response:
            if response.status == 200:
                json_data = await response.json()
                search_results = json_data.get("results", [])

                # 검색 결과를 URL 필터링하여 반환
                search_results = self._filter_results(search_results)
            else:
                print(f"Failed to fetch results from Tavily. Status: {response.status}")

        return search_results
    
    def _filter_results(self, results: List[dict]) -> List[str]:
        """
        검색 결과에서 포함할 URL과 제외할 URL 조건에 따라 필터링합니다.
        :param results: 검색 결과 리스트 (딕셔너리 형식)
        :return: 필터링된 검색 결과의 URL 리스트
        """
        filtered_results = []
        for result in results:
            url = result.get('url', '')
            
            # 포함할 URL이 있을 경우 해당 URL을 포함하지 않으면 패스
            if self.include_urls and not any(include_url in url for include_url in self.include_urls):
                continue
            
            # 제외할 URL이 있을 경우 해당 URL이 포함되면 패스
            if any(exclude_url in url for exclude_url in self.exclude_urls):
                continue
            
            # URL 필터링 조건을 통과한 경우 결과에 추가
            filtered_results.append(url)
        
        return filtered_results

    async def fetch_full_text(self, url: str) -> Optional[str]:
        """
        주어진 URL에서 해당 웹 페이지의 내용을 가져옵니다.
        PDF 또는 HTML 내용을 파싱하여 텍스트를 추출할 수 있습니다.
        :param url: 텍스트를 추출할 웹 페이지의 URL
        :return: 해당 URL에서 추출한 텍스트 (성공 시) 또는 None (실패 시)
        """
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    content_type = response.headers.get('Content-Type', '')
                    if 'text/html' in content_type:
                        # HTML 텍스트 파싱 (예시)
                        text = await response.text()
                        return self._extract_text_from_html(text)
                    elif 'application/pdf' in content_type:
                        # PDF 파일 처리
                        pdf_data = await response.read()
                        return self._extract_text_from_pdf(pdf_data)
                else:
                    print(f"Failed to fetch {url}. Status code: {response.status}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None

    def _extract_text_from_html(self, html_content: str) -> str:
        """
        HTML 내용에서 텍스트를 추출하는 도우미 함수
        :param html_content: HTML 페이지의 소스 코드
        :return: 텍스트로 변환된 HTML 내용
        """
        # BeautifulSoup을 사용
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator="\n").strip()

    def _extract_text_from_pdf(self, pdf_data: bytes) -> str:
        """
        PDF 파일에서 텍스트를 추출하는 도우미 함수
        :param pdf_data: PDF 파일의 바이너리 데이터
        :return: 텍스트로 변환된 PDF 내용
        """
        try:
            from io import BytesIO
            from PyPDF2 import PdfReader
            
            pdf_reader = PdfReader(BytesIO(pdf_data))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

        filtered_results = []
        for result in results:
            url = result.get('url', '')
            
            # 포함할 URL이 있을 경우 해당 URL을 포함하지 않으면 패스
            if self.include_urls and not any(include_url in url for include_url in self.include_urls):
                continue
            
            # 제외할 URL이 있을 경우 해당 URL이 포함되면 패스
            if any(exclude_url in url for exclude_url in self.exclude_urls):
                continue
            
            # URL 필터링 조건을 통과한 경우 결과에 추가
            filtered_results.append(url)
        
        return filtered_results

    async def fetch_full_text(self, url: str) -> Optional[str]:
        """
        주어진 URL에서 해당 웹 페이지의 내용을 가져오기
        PDF 또는 HTML 내용을 파싱하여 텍스트를 추출할 수 있음
        :param url: 텍스트를 추출할 웹 페이지의 URL
        :return: 해당 URL에서 추출한 텍스트 (성공 시) 또는 None (실패 시)
        """
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    content_type = response.headers.get('Content-Type', '')
                    if 'text/html' in content_type:
                        # HTML 텍스트 파싱 (예시)
                        text = await response.text()
                        return self._extract_text_from_html(text)
                    elif 'application/pdf' in content_type:
                        # PDF 파일 처리
                        pdf_data = await response.read()
                        return self._extract_text_from_pdf(pdf_data)
                else:
                    print(f"Failed to fetch {url}. Status code: {response.status}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None

    def _extract_text_from_html(self, html_content: str) -> str:
        """
        HTML 내용에서 텍스트를 추출하는 도우미 함수
        :param html_content: HTML 페이지의 소스 코드
        :return: 텍스트로 변환된 HTML 내용
        """
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator="\n").strip()

    def _extract_text_from_pdf(self, pdf_data: bytes) -> str:
        """
        PDF 파일에서 텍스트를 추출하는 도우미 함수
        :param pdf_data: PDF 파일의 바이너리 데이터
        :return: 텍스트로 변환된 PDF 내용
        """
        # PyPDF2와 같은 라이브러리를 사용하여 PDF 텍스트 추출
        try:
            from io import BytesIO
            from PyPDF2 import PdfReader
            
            pdf_reader = PdfReader(BytesIO(pdf_data))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
