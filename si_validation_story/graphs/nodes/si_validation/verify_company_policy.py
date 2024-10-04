from ..common.models import *
from ..common.prompts import verify_company_policy_prompt
from ..common.agents import BasicChain, RAGAgent
from .si_validation_state import State
import glob

# ========== 수정 예정(대현님) ==========
class VerifyCompanyPolicy:
    def __init__(self):
        self.llm = gemini_1_5_flash
        self.prompt = verify_company_policy_prompt
        self.chain = BasicChain(llm = self.llm, prompt = self.prompt, input_variables=["si_data"])
        self.rag_agent = RAGAgent(prompt=self.prompt, llm=self.llm)

    def __call__(self, state: State) -> State:
        """
        Function to validate shipping instruction data against compliance.
        Args:
            state (State): The state object containing si_data and other information.
        
        Returns:
            State: Updated state with compliance validation result.
        """
        try:
            response = self.rag_agent.invoke({"si_data": state['si_data']})
            state['policy_answer'] = response
        except Exception as e:
            state['policy_answer'] = f"Error during compliance validation: {e}"
        state['next'] = "search_news"
        return state