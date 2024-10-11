import nest_asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .nodes.si_intake import si_intake_state, get_bkg, get_si, check_missing_data, generate_intake_report
from langgraph.graph import StateGraph, END

# Jupyter 환경에서 비동기 루프 중첩을 허용
nest_asyncio.apply()

# FastAPI 앱 선언
app = FastAPI()

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
        bkg_data = result['bkg_data']
        if isinstance(bkg_data, dict):
            return {"bkg_data": bkg_data}
        else:
            raise HTTPException(status_code=400, detail="Error retrieving BKG data.")

    def get_si_node_with_callback(self, state):
        result = self.get_si_node(state)
        si_data = result['si_data']
        if isinstance(si_data, dict):
            return {"si_data": si_data}
        else:
            raise HTTPException(status_code=400, detail="Error retrieving SI data.")

    def check_missing_data_node_with_callback(self, state):
        result = self.check_missing_data_node(state)
        return {"missing_answer": result['missing_answer']}

    def generate_intake_report_node_with_callback(self, state):
        result = self.generate_intake_report_node(state)
        return result

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