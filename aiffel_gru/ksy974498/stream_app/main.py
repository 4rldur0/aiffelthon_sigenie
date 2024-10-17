# main.py

from typing import Annotated

from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, ToolMessage
from ch1 import graph
from ch2 import graph as graph2

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서의 접근 허용 (배포 시엔 도메인을 명시하세요)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/streaming_sync/chat/ch1")
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
                        data_str = f"data: {message.content}"
                        yield f"{event_str}\n{data_str}\n\n"

        except Exception as e:
            yield f"data: {str(e)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/streaming_sync/chat/ch2")
def streaming_sync_chat(query: str):
    initial_state = {"messages": [HumanMessage(content=query)]}
    
    def event_stream():
        # try:
        for chunk in graph2.stream(initial_state):
            for node_name, node_results in chunk.items():
                chunk_messages = node_results.get("messages", [])
                for message in chunk_messages:
                    # You can have any logic you like here
                    # The important part is the yield
                    if not message:
                        continue
                    
                    event_str = f"event: {node_name}"
                    data_str = f"data: {message.content}"
                    yield f"{event_str}\n{data_str}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")



import uvicorn
# FastAPI 실행
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)