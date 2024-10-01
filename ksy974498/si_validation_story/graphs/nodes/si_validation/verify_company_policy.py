from ..common.models import *
from ..common.prompts import verify_company_policy_prompt
from ..common.agents import BasicChain, RAGAgent
from .si_validation_state import State
import glob

# ========== 수정 예정(대현님) ==========
class VerifyCompanyPolicy:
    def __init__(self):
        self.llm = gpt_4o_mini
        self.prompt = verify_company_policy_prompt
        self.chain = BasicChain(llm = self.llm, prompt = self.prompt, input_variables=["si_data"])
        self.rag = self.get_RAG_agent()

    def get_RAG_agent(self):
        urls = [
            "https://www.ilovesea.or.kr/dictionary/list.do",  # Replace with your URLs
        ]
        pdf_files = glob.glob('./docs/*.pdf')  # Adjust path to your PDF files
        sources = pdf_files + urls
        rag = RAGAgent(sources=sources, generate_response_chain=self.chain)
        return rag

    def __call__(self, state: State) -> State:
        """
        Function to validate shipping instruction data against compliance.
        Args:
            state (State): The state object containing si_data and other information.
        
        Returns:
            State: Updated state with compliance validation result.
        """
        try:
            response = self.rag.invoke({"si_data": state['si_data']})
            state['policy_answer'] = response
        except Exception as e:
            state['policy_answer'] = f"Error during compliance validation: {e}"
        state['next'] = "search_news"
        return state