import streamlit as st

def create_storyboard(agents, prompts, llms):
    st.title("ContainerGenie.ai Story Board")
    
    # 노드 추가/삭제를 위한 버튼
    if st.button("Add Node"):
        st.session_state['nodes'].append({'agent': agents, 'prompt': prompts, 'llm': llms})
    
    if st.button("Delete Last Node"):
        if st.session_state['nodes']:
            st.session_state['nodes'].pop()
    
    # 노드 표시
    if st.session_state.get('nodes', []):
        for i, node in enumerate(st.session_state['nodes']):
            st.write(f"Node {i+1}: Agent - {node['agent']}, Prompt - {node['prompt']}, LLM - {node['llm']}")
            st.write(f"Prompt: {node['prompt']}")
    
    if st.button("Generate Story"):
        st.write("Story Generated!")

# Story Execution Function
def execute_story():
    st.title("Story Execution")
    
    for i, node in enumerate(st.session_state['nodes']):
        st.write(f"Executing Node {i+1}: Agent - {node['agent']}")
        # 여기서 실제 작업을 실행하는 함수 호출 가능
        # 예: MongoDB에서 데이터 검색 또는 LLM을 통해 질의 처리
        st.write(f"Prompt: {node['prompt']}")
        
        result = f"Executed {node['agent']} with prompt: {node['prompt']}"
        st.success(result)

# Session 상태 초기화
if 'nodes' not in st.session_state:
    st.session_state['nodes'] = []