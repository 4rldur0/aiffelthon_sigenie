from .nodes.si_intake import si_intake_state, get_bkg, get_si, check_missing_data, generate_intake_report
from langgraph.graph import StateGraph, END

class SIIntake:
    def __init__(self):
        self.get_bkg_node = get_bkg.GetBKG()
        self.get_si_node = get_si.GetSI()
        self.check_missing_data_node = check_missing_data.CheckMissingData()
        self.generate_intake_report_node = generate_intake_report.GenerateIntakeReport()
        self.graph = self.generate_graph()
        self.state = si_intake_state.State()

    def generate_graph(self):
        workflow = StateGraph(si_intake_state.State)

        # Add nodes
        workflow.add_node("get_bkg", self.get_bkg_node)
        workflow.add_node("get_si", self.get_si_node)
        workflow.add_node("check_missing_data", self.check_missing_data_node)
        workflow.add_node("generate_intake_report", self.generate_intake_report_node)

        # Add edges
        workflow.set_entry_point("get_bkg")
        workflow.add_conditional_edges(
            "get_bkg", 
            lambda state: state['next'],
            {
                "get_si": "get_si", 
                "end": END
            }
        )
        workflow.add_conditional_edges(
            "get_si", 
            lambda state: state['next'],
            {
                "check_missing_data": "check_missing_data", 
                "end": END
            }
        )
        workflow.add_edge("check_missing_data", "generate_intake_report")
        workflow.add_edge("generate_intake_report", END)

        return workflow.compile()
    
    def invoke(self):
        return self.graph.invoke(self.state)