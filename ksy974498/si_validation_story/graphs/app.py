# import nest_asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from nodes.si_intake import si_intake_state, get_bkg, get_si, check_missing_data, generate_intake_report
from langgraph.graph import StateGraph, END
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
import asyncio

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서의 접근 허용 (배포 시엔 도메인을 명시하세요)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 전역 상태 저장소 (state store)
STATE_STORE = {}

class SIIntake:
    def __init__(self):
        self.get_bkg_node = get_bkg.GetBKG()
        self.get_si_node = get_si.GetSI()
        self.check_missing_data_node = check_missing_data.CheckMissingData()
        self.generate_intake_report_node = generate_intake_report.GenerateIntakeReport()
        self.graph = self.generate_graph()

        # 상태 초기화
        self.state = si_intake_state.State()

        self.steps = ["Get BKG", "Get SI", "Check Missing Data", "Generate Intake Report"]
        self.current_step = 0

    def generate_graph(self):
        workflow = StateGraph(si_intake_state.State)
        workflow.add_node("get_bkg", self.get_bkg_node_with_callback)
        workflow.add_node("get_si", self.get_si_node_with_callback)
        workflow.add_node("check_missing_data", self.check_missing_data_node_with_callback)
        workflow.add_node("generate_intake_report", self.generate_intake_report_node_with_callback)

        workflow.set_entry_point("get_bkg")
        workflow.add_conditional_edges("get_bkg", lambda state: state['next'], {"get_si": "get_si", "end": END})
        workflow.add_conditional_edges("get_si", lambda state: state['next'], {"check_missing_data": "check_missing_data", "end": END})
        workflow.add_edge("check_missing_data", "generate_intake_report")
        workflow.add_edge("generate_intake_report", END)
        return workflow.compile()

    def get_bkg_node_with_callback(self, state):
        result = self.get_bkg_node(state)
        bkg_data = str(result['bkg_data'])
        return {"bkg_data": bkg_data}

    def get_si_node_with_callback(self, state):
        result = self.get_si_node(state)
        si_data = str(result['si_data'])
        return {"si_data": si_data}

    def check_missing_data_node_with_callback(self, state):
        result = self.check_missing_data_node(state)
        return {"missing_answer": result['missing_answer']}

    def generate_intake_report_node_with_callback(self, state):
        result = self.generate_intake_report_node(state)
        return {"intake_report": result['summary_answer']}

    def invoke(self, state):
        return self.graph.invoke(state)

class BookingReferenceModel(BaseModel):
    booking_reference: str

si_intake_process = SIIntake()

@app.post("/start_process/")
async def start_process(data: BookingReferenceModel):
    booking_reference = data.booking_reference
    if booking_reference not in STATE_STORE:
        state = si_intake_state.State()
        state['booking_reference'] = booking_reference
        STATE_STORE[booking_reference] = state
    else:
        raise HTTPException(status_code=400, detail="Process already started for this booking reference.")
    return {"message": "Process started", "booking_reference": booking_reference}

@app.post("/step/{step_name}")
async def run_step(step_name: str, data: BookingReferenceModel):
    booking_reference = data.booking_reference
    if booking_reference not in STATE_STORE:
        raise HTTPException(status_code=404, detail="Booking reference not found.")
    
    state = STATE_STORE[booking_reference]

    if step_name == "get_bkg":
        result = si_intake_process.get_bkg_node_with_callback(state)
    elif step_name == "get_si":
        result = si_intake_process.get_si_node_with_callback(state)
    elif step_name == "check_missing_data":
        result = si_intake_process.check_missing_data_node_with_callback(state)
    elif step_name == "generate_intake_report":
        result = si_intake_process.generate_intake_report_node_with_callback(state)
    else:
        raise HTTPException(status_code=400, detail="Invalid step name provided.")

    STATE_STORE[booking_reference] = state
    return result

# 스트리밍 함수
async def stream_result(state, step_name) -> AsyncGenerator[str, None]:
    steps = {
        "get_bkg": si_intake_process.get_bkg_node_with_callback,
        "get_si": si_intake_process.get_si_node_with_callback,
        "check_missing_data": si_intake_process.check_missing_data_node_with_callback,
        "generate_intake_report": si_intake_process.generate_intake_report_node_with_callback,
    }
    
    if step_name not in steps:
        raise HTTPException(status_code=400, detail="Invalid step name provided.")

    # 각 단계 실행 결과 스트리밍
    result = steps[step_name](state)
    yield f"{step_name} result: {result}\n"
    await asyncio.sleep(1)  # 비동기 딜레이 추가

@app.post("/stream_step/{step_name}")
async def stream_step(step_name: str, data: BookingReferenceModel):
    booking_reference = data.booking_reference
    if booking_reference not in STATE_STORE:
        raise HTTPException(status_code=404, detail="Booking reference not found.")
    
    state = STATE_STORE[booking_reference]

    # 스트리밍 응답 생성
    return StreamingResponse(stream_result(state, step_name), media_type="text/plain")

@app.post("/finish_process/")
async def finish_process(data: BookingReferenceModel):
    booking_reference = data.booking_reference
    if booking_reference not in STATE_STORE:
        raise HTTPException(status_code=404, detail="Booking reference not found.")
    
    del STATE_STORE[booking_reference]
    
    return {"message": "Process finished and state cleared."}


from starlette.responses import StreamingResponse
from fastapi import FastAPI, Query
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()

# 프롬프트 템플릿 설정
template = "{query}"
prompt = PromptTemplate.from_template(template=template)
llm = ChatOpenAI(temperature=0, 
                    model_name="gpt-4o-mini",
                    streaming=True,
                    )

@app.get("/chat")
def sync_chat(query: str):
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"query": query})

@app.get("/streaming/chat")
def streaming_sync_chat(query: str):
    chain = prompt | llm | StrOutputParser()

    def event_stream():
        try:
            for chunk in chain.stream({"query": query}):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: error : {str(e)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# FastAPI 실행
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)