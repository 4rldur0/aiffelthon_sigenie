from ..common.models import *
from ..common.prompts import intake_report_prompt
from .si_intake_state import State

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from ..common.schemas import ShipmentSummary

class GenerateIntakeReport:
    def __init__(self):
        self.output_parser = JsonOutputParser(pydantic_object=ShipmentSummary)
        self.llm = gpt_4o_mini
        self.prompt = PromptTemplate(
            template=intake_report_prompt,
            input_variables=["si_data", "missing_info"],
            partial_variables={
                "format_instructions": self.output_parser.get_format_instructions()
            },
        )
        self.chain = self.prompt | self.llm | self.output_parser

    def __call__(self, state: State) -> State:
        try:
            response = self.chain.invoke(
                {   
                    "si_data" : state['si_data'],
                    "missing_info": state["missing_answer"],
                }
            )
            state['summary_answer'] = response
        except Exception as e:
            state['summary_answer'] = f"Error generating summary: {e}"
        return state