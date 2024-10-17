# main.py

from typing import Annotated

from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, ToolMessage
from llm_flow import graph

app = FastAPI()

def event_stream(si_data: str):
    initial_state = {"messages": [HumanMessage(content=si_data)]}
    for chunk in graph.stream(initial_state):
        for node_name, node_results in chunk.items():
            chunk_messages = node_results.get("messages", [])
            for message in chunk_messages:
                # You can have any logic you like here
                # The important part is the yield
                if not message:
                    continue
                
                event_str = f"event: {node_name}"
                data_str = f"data: {message}"
                yield f"{event_str}\n{data_str}\n\n"

@app.post("/stream")
async def stream(query: Annotated[str, Body(embed=True)]):
    return StreamingResponse(event_stream(query), media_type="text/event-stream")

@app.get("/streaming_sync/chat")
def streaming_sync_chat(query: str):
    initial_state = {"messages": [HumanMessage(content=query)]}
    
    def event_stream():
        try:
            for chunk in graph.stream(initial_state):
                for node_name, node_results in chunk.items():
                    chunk_messages = node_results.get("messages", [])
                    for message in chunk_messages:
                        # You can have any logic you like here
                        # The important part is the yield
                        if not message:
                            continue
                        
                        event_str = f"event: {node_name}"
                        data_str = f"data: {message}"
                        yield f"{event_str}\n{data_str}\n\n"

        except Exception as e:
            yield f"data: {str(e)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

import uvicorn
# FastAPI 실행
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)