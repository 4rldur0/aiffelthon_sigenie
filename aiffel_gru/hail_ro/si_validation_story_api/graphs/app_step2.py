import nest_asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import streamlit as st
from nodes.si_validation import si_validation_state, check_parties, verify_company_policy, verify_vessel_port_situation, generate_validation_report
from langgraph.graph import StateGraph, END

# Jupyter 환경에서 비동기 루프 중첩을 허용
nest_asyncio.apply()

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


class SIValidation:
    def __init__(self):
        self.check_parties_node = check_parties.CheckParties()
        self.verify_company_policy_node = verify_company_policy.VerifyCompanyPolicy()
        self.verify_vessel_port_situation_node = verify_vessel_port_situation.VerifyVesselPortSituation()
        self.generate_validation_report_node = generate_validation_report.GenerateValidationReport()
        self.graph = self.generate_graph()

        self.state = si_validation_state.State()

        self.steps = ["Check Parties", "Verify Company Policy", "Verify Vessel&Port Situation", "Generate Validation Report"]
        self.total_steps = len(self.steps)
        self.current_step = 0

    def generate_graph(self):
        workflow = StateGraph(si_validation_state.State)

        # Add nodes
        workflow.add_node("check_parties", self.check_parties_node_with_callback)
        workflow.add_node("verify_company_policy", self.verify_company_policy_node_with_callback)
        workflow.add_node("verify_vessel_port_situation", self.verify_vessel_port_situation_node_with_callback)
        workflow.add_node("generate_validation_report", self.generate_validation_report_node_with_callback)

        # Add edges
        workflow.set_entry_point("check_parties")
        workflow.add_edge("check_parties", "verify_company_policy")
        workflow.add_edge("verify_company_policy", "verify_vessel_port_situation")
        workflow.add_edge("verify_vessel_port_situation", "generate_validation_report")
        workflow.add_edge("generate_validation_report", END)

        return workflow.compile()

    def check_parties_node_with_callback(self, state):
        result = self.check_parties_node(state)
        parties_answer = str(result['parties_answer'])
        return {"parties_answer": parties_answer}

    def verify_company_policy_node_with_callback(self, state):
        result = self.verify_company_policy_node(state)
        policy_answer = str(result['policy_answer'])
        return {"policy_answer": policy_answer}

    def verify_vessel_port_situation_node_with_callback(self, state):
        result = self.verify_vessel_port_situation_node(state)
        news_answer = str(result['news_answer'])
        return {"news_answer": news_answer}

    def generate_validation_report_node_with_callback(self, state):
        result = self.generate_validation_report_node(state)
        summary_answer = str(result['summary_answer'])
        return {"summary_answer": summary_answer}

    def invoke(self):
        return self.graph.invoke(self.state)

class BookingReferenceModel(BaseModel):
    booking_reference: str

si_validation_process = SIValidation()

@app.post("/start_process/")
async def start_process(data: BookingReferenceModel):
    booking_reference = data.booking_reference
    if booking_reference not in STATE_STORE:
        state = si_validation_state.State()
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

    if step_name == "check_parties":
        result = si_validation_state.check_parties_node_with_callback(state)
    elif step_name == "verify_company_policy":
        result = si_validation_state.verify_company_policy_node_with_callback(state)
    elif step_name == "verify_vessel_port_situation":
        result = si_validation_state.verify_vessel_port_situation_node_with_callback(state)
    elif step_name == "generate_validation_report":
        result = si_validation_state.generate_validation_report_node_with_callback(state)
    else:
        raise HTTPException(status_code=400, detail="Invalid step name provided.")

    STATE_STORE[booking_reference] = state
    return result

@app.post("/finish_process/")
async def finish_process(data: BookingReferenceModel):
    booking_reference = data.booking_reference
    if booking_reference not in STATE_STORE:
        raise HTTPException(status_code=404, detail="Booking reference not found.")
    
    del STATE_STORE[booking_reference]
    
    return {"message": "Process finished and state cleared."}

# FastAPI 실행
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)