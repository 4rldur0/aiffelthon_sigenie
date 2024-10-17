from ..common.models import *
from ..common.prompts import check_missing_prompt
from .si_intake_state import State

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from ..common.schemas import ShipmentStatus

class CheckMissingData:
    def __init__(self):
        self.output_parser = JsonOutputParser(pydantic_object=ShipmentStatus)
        self.llm = gpt_4o_mini
        self.prompt = PromptTemplate(
            template=check_missing_prompt,
            input_variables=["si_data"],
            partial_variables={
                "format_instructions": self.output_parser.get_format_instructions()
            },
        )
        self.chain = self.prompt | self.llm | self.output_parser
    
    def __call__(self, state: State) -> State:
        try:
            # Synchronously invoke the LLM to check for missing data
            response = self.chain.invoke({"si_data": state["si_data"]})
            state['missing_answer'] = response
        except Exception as e:
            state['missing_answer'] = f"Error during checking missing data: {e}"
        state['next'] = "generate_intake_report"
        return state