import streamlit as st

def sidebar():
    st.sidebar.title("ContainerGenie.ai")
    
    # Available Agents, Prompts, LLM, Dataset 선택 옵션 추가
    st.sidebar.subheader("Available Agent and Configuration")
    agents = st.sidebar.multiselect('Select Agents', ['MongoDB', 'Validator', 'Web Search', 'RAG'])
    
    st.sidebar.subheader("Available Prompt and Configuration")
    prompts = st.sidebar.multiselect('Select Prompts', ['Booking', 'Shipping', 'SI'])
    
    st.sidebar.subheader("Available LLM and Configuration")
    llms = st.sidebar.multiselect('Select LLM', ['ChatGPT', 'Llama', 'RAG (web)', 'RAG (no-web)'])
    
    st.sidebar.subheader("Import/Export Dataset")
    datasets = st.sidebar.file_uploader("Upload Dataset", type=["csv", "xlsx", "json"])
    
    return agents, prompts, llms, datasets