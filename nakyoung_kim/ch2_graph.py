import os
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, TypedDict
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import StrOutputParser
from langchain.agents.agent_types import AgentType

# Initialize Groq LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.0)

# Create pandas dataframe agent
if isinstance(llm, ChatOpenAI):
    pandas_agent = create_pandas_dataframe_agent(
        llm,
        coastal_schedule,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code=True
    )
else:
    pandas_agent = create_pandas_dataframe_agent(
        llm,
        coastal_schedule,
        verbose=True,
        allow_dangerous_code=True
    )

# Define the prompt templates
# ============= 프롬프트 교체 예정 =============
example_prompt = """ You are a container vessel schedule expert with deep knowledge of maritime operations. You have access to a dataframe containing information about vessel voyages, schedules, and performance metrics.

Use the following information to answer the user's question in detail:
1. The user's question is provided in the {question} placeholder. Make sure to address this question directly in your response.
2. The pandas agent has performed calculations or data manipulations based on the question. The results are provided in the {pandas_response} placeholder. Use this information to support your analysis.
3. If the pandas agent encountered an error, explain what might have caused it and suggest alternative approaches.
4. Provide clear and concise answers, using bullet points where appropriate.
5. If the question is unclear, ask for clarification.
6. If the answer requires comparing multiple voyages or summarizing trends, make sure to highlight key findings.
7. Include relevant statistics or metrics from the dataframe to support your answer.
8. If you don't know the answer or if the required data is not in the dataframe, say so honestly.
9. If {question} is delated to DELAY, check If DELAY_ETA is greater than 0.

Dataframe column descriptions:
SERVICE: service where the vessel is deployed
VESSEL: vessel full name
VOYAGE: voyage number with direction code
PORT: calling port name
TERMINAL: berthing terminal in the calling port
LONG_TERM_SCHEDULE_ETA: estimated time of arrival per long term schedule
LONG_TERM_SCHEDULE_ETB: estimated time of berth per long term schedule
LONG_TERM_SCHEDULE_ETD: estimated time of departure per long term schedule
COASTAL_SCHEDULE_ETA: estimated time of arrival per coastal schedule
COASTAL_SCHEDULE_ETB: estimated time of berth per coastal schedule
COASTAL_SCHEDULE_ETD: estimated time of departure per coastal schedule
DELAY_ETA: delays in arrival by the coastal schedule against long term schedule
DELAY_ETB: delays in berth by the coastal schedule against long term schedule
DELAY_ETD: delays in departure by the coastal schedule against long term schedule
ZD: zone description
PILOT_IN: pilot in time between arrival to berth
PILOT_OUT: pilot out time between unberth to pilot left
BERTH_HOUR: berthing hours between berthing to unberthing
DISTANCE: distance in nautical miles between calling port to next calling port
SEA_SPEED: speed in knots for sailing between calling port to next calling port

Question: {question}

Pandas Agent Response: {pandas_response}

Answer: """
# Create the prompts
example_prompt = ChatPromptTemplate.from_template(example_prompt)

# ============= chain 정의 예시 =============
# Create the chains
example_chain = example_prompt | llm | StrOutputParser()

# Define the state
class State(TypedDict):
    question: str
    answer: str
    raw_data: str
    next: str

# Define the nodes
# ============= 인섭님 =============
def load_si(state: State) -> State:
    # raw_data에 si 저장
    return state
# ============= 대현님 =============
def check_policy(state: State) -> State:
    # answer에 답변 저장
    return state
# ============= 미정 =============
def check_streaming_data(state: State) -> State:
    # answer에 답변 저장
    return state
# ============= 성연님 =============
def summary_report(state: State) -> State:
    # answer 정보 정리
    return state

# Create the graph
workflow = StateGraph(State)

# Add nodes
workflow.add_node("load_si", load_si)
workflow.add_node("check_policy", check_policy)
workflow.add_node("check_streaming_data", check_streaming_data)
workflow.add_node("summary_report", summary_report)

# Add edges
workflow.set_entry_point("load_si")
workflow.add_edge("load_si", "check_policy")
workflow.add_edge("check_policy", "check_streaming_data")
workflow.add_edge("check_streaming_data", "summary_report")
workflow.add_edge("summary_report", END)

# Compile the graph
app = workflow.compile()

# Function for processing main workflows
def ch2_monitor(prompt: str):
    response = app.invoke({
        "question": prompt,
        # "answer": "",
        # "raw_data": "",
        # "next": ""
    })
    return response['answer']

# Run the main functions
def run():
    return coastal_monitor

# Run the streamlit function
if __name__ == "__main__":
    run()