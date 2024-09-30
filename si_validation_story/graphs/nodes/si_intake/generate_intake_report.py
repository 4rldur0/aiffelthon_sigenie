from ..common.models import *
from ..common.prompts import validation_report_prompt
from ..common.agents import BasicChain
from .si_intake_state import State

class GenerateIntakeReport:
    def __init__(self):
        self.llm = gpt_4o_mini
        self.prompt = validation_report_prompt
        self.chain = BasicChain(llm = self.llm, prompt = self.prompt, input_variables=["si_data"])

    def __call__(self, state: State) -> State:
        try:
            response = self.chain.invoke(
                {"si_data": state["si_data"]}
            )
            state['summary_answer'] = response
        except Exception as e:
            state['summary_answer'] = f"Error generating summary: {e}"
        return state
