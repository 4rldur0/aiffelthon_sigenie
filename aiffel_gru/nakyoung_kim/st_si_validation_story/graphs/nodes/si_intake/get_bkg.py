from ..common.tools import MongoDB
from .si_intake_state import State

class GetBKG:
    def __init__(self):
        self.mongodb = MongoDB(collection_name="bkg")
    
    def __call__(self, state: State) -> State:
        bkg_data = self.mongodb.find_one_booking_reference(state["booking_reference"])
        if bkg_data is None:
            state["bkg_data"] = "No Booking Data found for the given booking reference"
            state["next"] = "end"
        else:
            state["bkg_data"] = bkg_data
            state["next"] = "get_si"
        return state