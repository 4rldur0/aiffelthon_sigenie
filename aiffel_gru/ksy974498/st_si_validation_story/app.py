from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.chains.sequential import SimpleSequentialChain
from graphs.nodes.si_intake import si_intake_state, get_bkg, get_si, check_missing_data, generate_intake_report

app = FastAPI()

# State management store (replace with proper session handling for production)
state_store = {}

class SIIntakeRequest(BaseModel):
    booking_reference: str
    state_id: str  # Unique identifier for state management

class StateProgress(BaseModel):
    state_id: str

class SIIntake:
    def __init__(self):
        self.state = None

    def initialize_state(self, booking_reference):
        # Initialize the state with a booking reference
        self.state = si_intake_state.State()
        self.state['booking_reference'] = booking_reference
        return self.state

    def get_bkg(self, state):
        result = get_bkg.GetBKG()(state)
        if 'bkg_data' in result:
            return result
        else:
            raise HTTPException(status_code=500, detail="Error retrieving BKG data")

    def get_si(self, state):
        result = get_si.GetSI()(state)
        if 'si_data' in result:
            return result
        else:
            raise HTTPException(status_code=500, detail="Error retrieving SI data")

    def check_missing_data(self, state):
        result = check_missing_data.CheckMissingData()(state)
        return result

    def generate_intake_report(self, state):
        result = generate_intake_report.GenerateIntakeReport()(state)
        return result


# Instantiate SIIntake
si_intake_instance = SIIntake()

# Define LangChain sequence for the SI intake process
def create_intake_chain():
    # LangChain's SimpleSequentialChain is used to link each step in sequence
    intake_chain = SimpleSequentialChain(
        chains=[
            lambda state: si_intake_instance.get_bkg(state),
            lambda state: si_intake_instance.get_si(state),
            lambda state: si_intake_instance.check_missing_data(state),
            lambda state: si_intake_instance.generate_intake_report(state)
        ],
        input_variables=["state"],  # Passing the state between steps
        verbose=True
    )
    return intake_chain

@app.post("/start_intake/")
async def start_intake(request: SIIntakeRequest):
    booking_reference = request.booking_reference
    state_id = request.state_id

    if not booking_reference:
        raise HTTPException(status_code=400, detail="Booking reference cannot be empty")

    # Initialize the state and store it globally
    state = si_intake_instance.initialize_state(booking_reference)
    state_store[state_id] = state

    return {"message": "Intake process started", "state_id": state_id}


@app.post("/step/get_bkg/")
async def step_get_bkg(request: StateProgress):
    state_id = request.state_id

    if state_id not in state_store:
        raise HTTPException(status_code=404, detail="State not found")

    state = state_store[state_id]

    # Execute the BKG step through LangChain
    result = si_intake_instance.get_bkg(state)

    # Store updated state
    state_store[state_id] = state

    return {"message": "BKG data retrieved", "bkg_data": result['bkg_data']}


@app.post("/step/get_si/")
async def step_get_si(request: StateProgress):
    state_id = request.state_id

    if state_id not in state_store:
        raise HTTPException(status_code=404, detail="State not found")

    state = state_store[state_id]

    # Execute the SI step through LangChain
    result = si_intake_instance.get_si(state)

    # Store updated state
    state_store[state_id] = state

    return {"message": "SI data retrieved", "si_data": result['si_data']}


@app.post("/step/check_missing_data/")
async def step_check_missing_data(request: StateProgress):
    state_id = request.state_id

    if state_id not in state_store:
        raise HTTPException(status_code=404, detail="State not found")

    state = state_store[state_id]

    # Execute the missing data check step through LangChain
    result = si_intake_instance.check_missing_data(state)

    # Store updated state
    state_store[state_id] = state

    return {"message": "Missing data check complete", "missing_answer": result['missing_answer']}


@app.post("/step/generate_report/")
async def step_generate_report(request: StateProgress):
    state_id = request.state_id

    if state_id not in state_store:
        raise HTTPException(status_code=404, detail="State not found")

    state = state_store[state_id]

    # Execute the report generation step through LangChain
    result = si_intake_instance.generate_intake_report(state)

    # Store updated state
    state_store[state_id] = state

    return {"message": "Intake report generated", "report": result}


@app.post("/run_full_intake/")
async def run_full_intake(request: StateProgress):
    state_id = request.state_id

    if state_id not in state_store:
        raise HTTPException(status_code=404, detail="State not found")

    state = state_store[state_id]

    # Run the full intake process using LangChain's chain
    intake_chain = create_intake_chain()
    result = intake_chain.run(state)

    # Update the state after full chain execution
    state_store[state_id] = state

    return {"message": "Full intake process completed", "result": result}