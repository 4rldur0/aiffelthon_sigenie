from ..common.models import *
from ..common.prompts import intake_report_prompt
from ..common.agents import BasicChain
from .si_intake_state import State

class GenerateIntakeReport:
    def __init__(self):
        self.llm = gemini_1_5_flash
        self.prompt = intake_report_prompt
        self.chain = BasicChain(llm = self.llm, prompt = self.prompt, input_variables=["sources"])

    def __call__(self, state: State) -> State:
        try:
            response = self.chain.invoke(
                {
                    "missing_info": state["missing_answer"],
                }
            )
            state['summary_answer'] = response
        except Exception as e:
            state['summary_answer'] = f"Error generating summary: {e}"
        return state
