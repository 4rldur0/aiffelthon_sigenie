from ..common.models import *
from ..common.prompts import check_parties_prompt
from ..common.agents import RAGAgent
from .si_validation_state import State

# ========= 수정 예정(인섭님) ==========
class CheckParties:
    def __init__(self):
        self.llm = gpt_4o_mini
        self.prompt = check_parties_prompt
        self.rag_agent = RAGAgent(prompt=self.prompt, llm=self.llm)

    def __call__(self, state: State) -> State:
        try:
            response = self.rag_agent.invoke({"si_data": state['si_data']})
            state['parties_answer'] = response
        except Exception as e:
            state['parties_answer'] = f"Error during checking parties: {e}"
        state['next'] = "validate_compliance"
        return state