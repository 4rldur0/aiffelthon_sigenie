from ..common.tools import MongoDB
from .si_intake_state import State

class GetBKG:
    def __init__(self):
        self.collection_name = "bkg"
        self.db = MongoDB()
        self.collection = self.db.load_collection(self.collection_name)
    
    def __call__(self, state: State) -> State:
        bkg_data = self.collection.find_one_booking_reference(state["booking_reference"])
        state["next"] = "get_si"
        return state