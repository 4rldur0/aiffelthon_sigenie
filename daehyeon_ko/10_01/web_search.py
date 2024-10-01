from tavily import TavilySearch
from typing import List, Dict

class WebSearch:
    """
    Web search class using Tavily for querying the web and filtering results.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize the WebSearch class with an optional API key.
        :param api_key: API key for Tavily web search (if required).
        """
        self.api_key = api_key
        self.searcher = TavilySearch(api_key=self.api_key)  # Initialize TavilySearch with the API key

    def search(self, query: str, include_urls: List[str] = None, exclude_urls: List[str] = None) -> List[Dict]:
        """
        Perform a web search with optional inclusion and exclusion of specific URLs using Tavily.
        :param query: The search query string.
        :param include_urls: A list of URLs to prioritize in search results.
        :param exclude_urls: A list of URLs to exclude from search results.
        :return: A list of dictionaries containing search results.
        """
        try:
            # Perform search with TavilySearch
            results = self.searcher.search(query)

            # Filter results based on include/exclude URL logic
            filtered_results = []
            for result in results:
                link = result.get('url', '')
                if include_urls and not any(url in link for url in include_urls):
                    continue
                if exclude_urls and any(url in link for url in exclude_urls):
                    continue
                filtered_results.append(result)

            return filtered_results
        except Exception as e:
            print(f"Error occurred during web search: {e}")
            return []
