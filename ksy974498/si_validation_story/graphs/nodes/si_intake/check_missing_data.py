from ..common.models import *
from ..common.prompts import check_missing_prompt
from ..common.agents import BasicChain
from .si_intake_state import State

class CheckMissingData:
    def __init__(self):
        self.llm = gemini_1_5_flash
        self.prompt = check_missing_prompt
        self.chain = BasicChain(llm = self.llm, prompt = self.prompt, input_variables=["si_data"])
    
    def __call__(self, state: State) -> State:
        try:
            # Synchronously invoke the LLM to check for missing data
            response = self.chain.invoke({"si_data": state["si_data"]})
            state['missing_answer'] = response
        except Exception as e:
            state['missing_answer'] = f"Error during checking missing data: {e}"
        state['next'] = "generate_intake_report"
        return state