import streamlit as st
from ._page_templates import BLDraftPage, ValReportPage
from graphs.st_si_validation_graph import SIValidation

graph = SIValidation()

def main():
    st.title("Ch 2: Shipping Instruction Validation")

    # chapter 1을 이미 실행 하였을 경우에만 chapter 2 진행 가능
    if "si_data" in st.session_state.keys() and st.session_state["si_data"]:
        # Chapter 2 그래프 인스턴스 생성
        # session 변수로 저장되어 있던 si_data를 그래프의 스테이트에 저장
        # chapter 1에서 찾은 si_data를 chapter 2로 전달
        graph.state["si_data"] = st.session_state["si_data"]
        
        # 그래프의 최종 출력(=그래프 스테이트)을 저장하기 위한 변수
        result = None
        
        # 그래프 invoke를 실행하는 버튼
        if st.button("Generate Report"):
            try:
                result = graph.invoke()
            except Exception as e:
                st.error(f"An error occurred while Invoking the shipping Instruction Validation Graph: {str(e)}")
                st.stop()
        
        # 그래프 최종 출력이 존재할 경우에만 실행
        if result is not None:
            # 그래프 스테이트로부터 si_data 가져옴
            si_data = result.get("si_data")
            if si_data:
                # draft B/L을 보여주는 페이지 인스턴스
                bl_draft_page = BLDraftPage(si_data=si_data)
                # report를 보여주는 페이지 인스턴스
                report_page = ValReportPage(report_name="Shipping Instruction Validation Report",
                                         text=result.get("summary_answer", "No summary available"))
                
                # 화면을 좌우로 나눔
                col1, col2 = st.columns(2)
                
                # 왼쪽 화면에는 draft B/L 출력
                with col1:
                    bl_draft_page.show_bl_draft_page()
                # 오른쪽 화면에는 report 출력
                with col2:
                    report_page.show_report_page()
        # 그래프 최종 출력이 올바르지 않을 때
        else:
            st.warning("Shipping Instruction data is required. Return to Chapter 1 to fetch the data first.")
    else:
        st.error("Shipping Instruction data is required. Return to Chapter 1 to fetch the data first.")