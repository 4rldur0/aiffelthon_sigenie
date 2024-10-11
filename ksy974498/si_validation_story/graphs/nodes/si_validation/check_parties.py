import os
from ..common.models import *
from ..common.prompts import check_parties_prompt
from ..common.agents import RAGAgent
from .si_validation_state import State

class CheckParties:
    def __init__(self):
        self.llm = gpt_4o_mini
        self.prompt = check_parties_prompt
        pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CHERRY_Shipping_Line_Company_Policy.pdf")
        self.rag_agent = RAGAgent(prompt=self.prompt, llm=self.llm, pdf_path=pdf_path)

    def __call__(self, state: State) -> State:
        try:
            response = self.rag_agent.invoke(state['si_data'])
            state['parties_answer'] = response
        except Exception as e:
            state['parties_answer'] = f"Error during checking parties: {e}"
        state['next'] = "validate_compliance"
        return state