from ..common.models import *
from ..common.prompts import check_missing_prompt
# from ..common.agents import BasicChain
from .si_intake_state import State

from langchain_core.output_parsers import JsonOutputParser
from ..common.schemas import ShipmentStatus
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

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
    

@app.get("/sync/chat")
def sync_chat(self, query: str = Query(None, min_length=3, max_length=50)):
    response = self.chain.invoke({"query": query})
    return response


@app.get("/streaming_async/chat")
async def streaming_async(query: str = Query(None, min_length=3, max_length=50)):
    async def event_stream():
        try:
            async for chunk in chain.astream({"query": query}):
                if len(chunk) > 0:
                    yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: {str(e)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")