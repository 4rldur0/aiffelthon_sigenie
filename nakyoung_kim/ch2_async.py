# Copyright (c) 2024 Tongyang Systems.
# All rights reserved.
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os
import pandas as pd
import asyncio
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document
from langchain.agents.agent_types import AgentType
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

# Load the dataframe
coastal_schedule = pd.read_csv('./data/coastal_schedule-Table 1.csv')

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

# Create the chains
prompt = """ 
Translate '{sentence}' to Korean 
Answer: """
prompt = ChatPromptTemplate.from_template(prompt)
chain = prompt | llm | StrOutputParser()

# Create the web search tool
web_search_tool = TavilySearchResults()

async def use_dataframe_tool(sentence):
    steps.append("use dataframe tool")
    try:
        result = await pandas_agent.ainvoke({
            "input": sentence
        })
        results.append(result)
    except Exception as e:
        result = f"Error occurred: {str(e)}"
    return {"result": result, "sentence": sentence, "steps": steps}

async def use_web_search(sentence):
    result=[]
    steps.append("use web search")
    web_results = await web_search_tool.ainvoke({
        "query": sentence
    })
    result.extend(
        [
            Document(page_content=d["content"], metadata={"url": d["url"]})
            for d in web_results
        ]
    )
    results.append(result)
    return {"result": result, "sentence": sentence, "steps": steps}

async def use_llm(sentence):
    steps.append("use llm")
    result = await chain.ainvoke({
        "sentence": sentence,
    })
    results.append(result)
    return {"result": result, "sentence": sentence, "steps": steps}

# Run 3 async chains
async def run_async():
    global results, steps
    results, steps = [], []
    outputs = await asyncio.gather(
        use_dataframe_tool("Is there a vessel to SHANGHAI?"),
        use_web_search("The world's largest seaport"),
        use_llm("Every cloud has a silver lining")
    )
    return outputs

# Run the streamlit function
if __name__ == "__main__":
    outputs = asyncio.run(run_async())
    print(outputs)
