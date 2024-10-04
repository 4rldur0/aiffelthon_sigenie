import streamlit as st
from ._page_templates import BLDraftPage, ReportPage
from graphs.si_intake_graph import SIIntake

# chapter 1 그래프 인스턴스 생성
graph = SIIntake()

def main():
    # booking reference를 사용자 입력으로 받음
    booking_reference = st.text_input("Enter Booking Reference")

    st.title("Ch1: Shipping Instruction Intake")
    # 그래프의 최종 출력(=그래프 스테이트)을 저장하기 위한 변수
    result = None
    # 그래프 invoke를 실행하는 버튼
    if st.button("Generate Report"):
        graph.state["booking_reference"] = booking_reference
        try:
            result = graph.invoke()
        except Exception as e:
            st.error(f"An error occurred while Searching the shipping Instruction: {str(e)}")
            st.stop()

    # 그래프 최종 출력이 존재할 경우에만 실행
    if result is not None:
        # 그래프 스테이트로부터 si_data 가져옴
        si_data = result.get("si_data")
        # streamlit session_state에 si_data 저장해놓음
        st.session_state["si_data"] = si_data

        if si_data:
            # draft B/L을 보여주는 페이지 인스턴스
            bl_draft_page = BLDraftPage(si_data=si_data)
            # report를 보여주는 페이지 인스턴스
            report_page = ReportPage(report_name="Shipping Instruction Validation Report",
                                     missing_answer=result.get("missing_answer", "No Missing Data available"),
                                     summary_answer=result.get("summary_answer", "No summary available"))

            # 화면을 좌우로 나눔
            col1, col2 = st.columns(2)

            # 왼쪽 화면에는 draft B/L 출력
            with col1:
                bl_draft_page.show_bl_draft_page()
            # 오른쪽 화면에는 report 출력
            with col2:
                report_page.show_report_page()
        # 그래프 최종 출력에서 si_data가 존재하지 않을 때
        else:
            st.warning("No shipping instruction data found for the given booking reference.")
    # 그래프 최종 출력이 존재하지 않을 때(=초기 화면)
    else:
        st.info("Please enter a booking reference first and click 'Generate Report' button.")