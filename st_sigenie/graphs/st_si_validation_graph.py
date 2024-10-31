import streamlit as st
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

    def update_progress(self, step_name):
        self.current_step += 1
        progress_value = self.current_step / self.total_steps
        self.progress_bar.progress(progress_value)
        self.status_text.text(f"Current step: {step_name} ({self.current_step}/{self.total_steps})")
        # 모든 단계가 완료되었을 때 나타나는 메세지
        if self.current_step == self.total_steps:
            self.status_text.text("SI Validation Process Completed! 🎉")

    def check_parties_node_with_callback(self, state):
        self.update_progress(self.steps[0])
        result = self.check_parties_node(state)
        with st.expander("View Check Parties Result", expanded=False):
            st.write(result['parties_answer']['output'])
        return result

    def verify_company_policy_node_with_callback(self, state):
        self.update_progress(self.steps[1])
        result = self.verify_company_policy_node(state)
        with st.expander("View Company Policy Result", expanded=False):
            st.write(result['policy_answer']['output'])
        return result

    def verify_vessel_port_situation_node_with_callback(self, state):
        self.update_progress(self.steps[2])
        result = self.verify_vessel_port_situation_node(state)
        with st.expander("View Vessel&Port Situation Result", expanded=False):
            st.json(result['news_answer'])
        return result

    def generate_validation_report_node_with_callback(self, state):
        self.update_progress(self.steps[3])
        result = self.generate_validation_report_node(state)
        return result

    def invoke(self):
        self.current_step = 0
        self.progress_bar = st.progress(0)
        self.status_text = st.empty()
        self.status_text.text(f"Starting SI Validation Process...")

        return self.graph.invoke(self.state)