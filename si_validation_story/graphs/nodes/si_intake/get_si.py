from ..common.tools import MongoDB
from .si_intake_state import State

class GetSI:
    def __init__(self):
        self.mongodb = MongoDB(collection_name="si")
    
    def __call__(self, state: State) -> State:
        si_data = self.mongodb.find_one_booking_reference(state["booking_reference"])
        if si_data is None:
            state["si_data"] = "No Shipping Instruction found for the given booking reference"
            state["next"] = "end"
        else:
            state["si_data"] = si_data
            state["next"] = "check_missing_data"
        return state