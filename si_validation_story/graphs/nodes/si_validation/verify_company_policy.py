import os
from ..common.models import *
from ..common.prompts import verify_company_policy_prompt
from ..common.agents import RAGAgent
from .si_validation_state import State

# ========== 수정 예정(대현님) ==========
class VerifyCompanyPolicy:
    def __init__(self):
        self.llm = gpt_4o_mini
        self.prompt = verify_company_policy_prompt
        pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CHERRY_Shipping_Line_Company_Policy.pdf")
        self.rag_agent = RAGAgent(prompt=self.prompt, llm=self.llm, pdf_path=pdf_path)

    def __call__(self, state: State) -> State:
        try:
            response = self.rag_agent.invoke(state['si_data'])
            state['policy_answer'] = response
        except Exception as e:
            state['policy_answer'] = f"Error during compliance validation: {e}"
        state['next'] = "search_news"
        return state