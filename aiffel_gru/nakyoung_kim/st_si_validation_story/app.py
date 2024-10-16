from layouts.pages import ch1_si_intake_page, ch2_si_validation_page
import streamlit as st

# 화면 분할을 위해 화면을 wide로 사용
st.set_page_config(layout="wide")

# chapter가 바뀔 때 session_state 변수(=si_data)를 저장해두기 위한 함수
def store_session_state_value():
    # 기존 session_state에 si_data가 존재한다면 이후 session_state에 해당 si_data를 새로 할당
    if "si_data" in st.session_state:
        st.session_state["si_data"] = st.session_state["si_data"]

def main():
    # chapter를 선택하는 사이드바 생성
    st.sidebar.title("Chapters")
    # chapter가 '바뀔 때' 위의 store_session_state_value() 함수가 실행됨
    chapter = st.sidebar.selectbox("Choose a chapter", 
                                    ["Ch 1: Shipping Instruction Intake", "Ch 2: Shipping Instruction Validation"],
                                    on_change=store_session_state_value)

    # chapter에 따라 다른 화면 페이지 나타남
    if chapter == "Ch 1: Shipping Instruction Intake":
        ch1_si_intake_page.main()
    elif chapter == "Ch 2: Shipping Instruction Validation":
        ch2_si_validation_page.main()

    # Footer 추가
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; padding: 10px;'>"
        "Copyright © 2024 SIGenie 0.02 - Early Access Version. All rights reserved."
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()