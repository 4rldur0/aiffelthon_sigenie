from ..common.tools import Tavily
from .si_validation_state import State

class VerifyVesselPortSituation:
    def __init__(self):
        self.web_search_tool = Tavily.web_search()
    # ====== 수정 예정 - 일단은 뉴스 웹검색으로 대체 ======
    def __call__(self, state: State) -> State:
        try:
            query = f"News about {state['si_data']['routeDetails']['portOfLoading']} port and {state['si_data']['routeDetails']['portOfDischarge']} port and {state['si_data']['voyageDetails']['vesselName']} vessel"
            response = self.web_search_tool.invoke(query)
            state['news_answer'] = response
        except Exception as e:
            state['news_answer'] = f"Error during searching news: {e}"
        state['next'] = "generate_summary"
        return state