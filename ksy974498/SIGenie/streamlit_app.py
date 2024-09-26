import streamlit as st

# 각 섹션을 함수로 정의
from sidebar import sidebar
from storyboard import create_storyboard, execute_story

def main():
    # 사이드바 구성
    agents, prompts, llms, datasets = sidebar()
    
    # 스토리보드 구성
    create_storyboard(agents, prompts, llms)
    
    # 스토리 실행
    if st.button("Run Story"):
        execute_story()

if __name__ == "__main__":
    main()