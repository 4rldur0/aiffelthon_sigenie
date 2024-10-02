from .nodes.si_validation import si_validation_state, check_parties, verify_company_policy, verify_vessel_port_situation, generate_validation_report
from langgraph.graph import StateGraph, END

class SIValidation:
    def __init__(self):
        self.check_parties_node = check_parties.CheckParties()
        self.verify_company_policy_node = verify_company_policy.VerifyCompanyPolicy()
        self.verify_vessel_port_situation_node = verify_vessel_port_situation.VerifyVesselPortSituation()
        self.generate_validation_report_node = generate_validation_report.GenerateValidationReport()
        self.graph = self.generate_graph()
        self.state = si_validation_state.State()

    def generate_graph(self):
        workflow = StateGraph(si_validation_state.State)

        # Add nodes
        workflow.add_node("check_parties", self.check_parties_node)
        workflow.add_node("verify_company_policy", self.verify_company_policy_node)
        workflow.add_node("verify_vessel_port_situation", self.verify_vessel_port_situation_node)
        workflow.add_node("generate_validation_report", self.generate_validation_report_node)

        # Add edges
        workflow.set_entry_point("check_parties")
        workflow.add_edge("check_parties", "verify_company_policy")
        workflow.add_edge("verify_company_policy", "verify_vessel_port_situation")
        workflow.add_edge("verify_vessel_port_situation", "generate_validation_report")
        workflow.add_edge("generate_validation_report", END)

        return workflow.compile()
    
    def invoke(self):
        return self.graph.invoke(self.state)