import streamlit as st
from utils.bill_of_lading import generate_bill_of_lading
# from utils.openai_llm import llm
from utils.templates import summary_template
import streamlit as st
import asyncio
from openai import AsyncOpenAI


async def generate_summary(placeholder, report):
    client = AsyncOpenAI()
    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": summary_template},
                  {"role": "user", "content": report},],
        stream=True
    )
    streamed_text = ""
    async for chunk in stream:
        chunk_content = chunk.choices[0].delta.content
        if chunk_content is not None:
            streamed_text = streamed_text + chunk_content
            placeholder.info(streamed_text)

def show_llm_summary_page():
    st.title("LLM Summary Report")
    box = st.empty()

    if "si_data" in st.session_state:
        si_data = st.session_state["si_data"]
        report = generate_bill_of_lading(si_data)

        if st.button("Generate LLM Enhanced Report"):
            asyncio.run(generate_summary(box, report))
    else:
        st.warning("Please search for a Shipping Instruction first.")