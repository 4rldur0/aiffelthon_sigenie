# main.py

import json
from ast import literal_eval
from typing import Annotated

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, ToolMessage
from ch1 import graph
from ch2 import graph as graph2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 허용할 도메인 설정
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메소드 설정
    allow_headers=["*"],  # 허용할 헤더 설정
)

# def event_stream(si_data: str):
#     initial_state = {"messages": [HumanMessage(content=si_data)]}
#     for chunk in graph.stream(initial_state):
#         for node_name, node_results in chunk.items():
#             chunk_messages = node_results.get("messages", [])
#             for message in chunk_messages:
#                 # You can have any logic you like here
#                 # The important part is the yield
#                 if not message:
#                     continue

#                 event_str = f"event: {node_name}"
#                 data_str = f"data: {message}"
#                 yield f"{event_str}\n{data_str}\n\n"

# @app.post("/stream")
# async def stream(query: Annotated[str, Body(embed=True)]):
#     return StreamingResponse(event_stream(query), media_type="text/event-stream")

@app.get("/streaming_sync/chat/ch1")
def streaming_sync_chat(query: str):
    initial_state = {"messages": [HumanMessage(content=query)]}

    def event_stream():
        try:
            for chunk in graph.stream(initial_state):
                for node_name, node_results in chunk.items():
                    chunk_messages = node_results.get("messages", [])
                    for message in chunk_messages:
                        if not message:
                            continue

                        if isinstance(message, HumanMessage):
                            content_dict = literal_eval(message.content)
                            content_str = json.dumps(content_dict)
                        else:
                            content_str = json.dumps(message)

                        event_str = f"event: {node_name}"
                        # id_str = f"id: {node_name}"
                        data_str = f"data: {content_str}"
                        yield f"{event_str}\n{data_str}\n\n"
                        # yield f"{id_str}\n{data_str}\n\n"

            yield "event: done\ndata: Response completed\n\n"

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

                    if isinstance(message, HumanMessage):
                        try:
                            content_dict = literal_eval(message.content)
                            content_str = json.dumps(content_dict)
                        except:
                            content_str = json.dumps({
                                'markdown': message.content
                            })
                    else:
                        content_str = json.dumps(message)

                    # event_str = f"event: {node_name}"
                    id_str = f"id: {node_name}"
                    data_str = f"data: {content_str}"
                    # yield f"{event_str}\n{data_str}\n\n"
                    yield f"{id_str}\n{data_str}\n\n"
        yield "event: done\ndata: Response completed\n\n"

        # except Exception as e:
        #     yield f"data: {str(e)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")



import uvicorn
# FastAPI 실행
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)