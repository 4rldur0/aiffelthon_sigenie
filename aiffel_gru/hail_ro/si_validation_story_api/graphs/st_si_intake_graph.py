import streamlit as st
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

        self.steps = ["Get BKG", "Get SI", "Check Missing Data", "Generate Intake Report"]
        self.total_steps = len(self.steps)
        self.current_step = 0

    def generate_graph(self):
        workflow = StateGraph(si_intake_state.State)

        # Add nodes with callbacks
        workflow.add_node("get_bkg", self.get_bkg_node_with_callback)
        workflow.add_node("get_si", self.get_si_node_with_callback)
        workflow.add_node("check_missing_data", self.check_missing_data_node_with_callback)
        workflow.add_node("generate_intake_report", self.generate_intake_report_node_with_callback)

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

    def update_progress(self, step_name):
        self.current_step += 1
        progress_value = self.current_step / self.total_steps
        self.progress_bar.progress(progress_value)
        self.status_text.text(f"Current step: {step_name} ({self.current_step}/{self.total_steps})")
        # 모든 단계가 완료되었을 때 나타나는 메세지
        if self.current_step == self.total_steps:
            self.status_text.text("SI Intake Process Completed! 🎉")

    def get_bkg_node_with_callback(self, state):
        self.update_progress(self.steps[0])
        result = self.get_bkg_node(state)
        bkg_data = result['bkg_data']
        if isinstance(bkg_data, dict):
            with st.expander("View Booking Data", expanded=False):
                st.json(bkg_data)
        else:
            st.error(bkg_data)
        return result

    def get_si_node_with_callback(self, state):
        self.update_progress(self.steps[1])
        result = self.get_si_node(state)
        si_data = result['si_data']
        if isinstance(si_data, dict):
            with st.expander("View Shipping Instruction", expanded=False):
                st.json(si_data)
        else :
            st.error(si_data)
        return result

    def check_missing_data_node_with_callback(self, state):
        self.update_progress(self.steps[2])
        result = self.check_missing_data_node(state)
        with st.expander("View Check Missing Result", expanded=False):
            st.write(result['missing_answer'])
        return result

    def generate_intake_report_node_with_callback(self, state):
        self.update_progress(self.steps[3])
        result = self.generate_intake_report_node(state)
        return result

    def invoke(self):
        self.current_step = 0
        self.progress_bar = st.progress(0)
        self.status_text = st.empty()
        self.status_text.text(f"Starting SI Intake Process...")

        return self.graph.invoke(self.state)