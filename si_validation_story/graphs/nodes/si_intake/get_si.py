from ..common.tools import MongoDB
from .si_intake_state import State

class GetSI:
    def __init__(self):
        self.collection_name = "si"
        self.db = MongoDB()
        self.collection = self.db.load_collection(self.collection_name)
    
    def __call__(self, state: State) -> State:
        si_data = self.collection.find_one_booking_reference(state["booking_reference"])
        state["si_data"] = si_data
        state["next"] = "check_missing_data"
        return state
