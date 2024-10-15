import asyncio  
from langchain.callbacks.base import BaseCallbackHandler  
from langchain.schema import LLMResult  
from langchain_openai import ChatOpenAI
from threading import Thread  
from queue import Queue  
from typing import Dict, List, Any  

class StreamingWrapper:
    def __init__(self):
        self.streamer_queue = Queue()  
        streaming_handler = self.StreamingHandler(self.streamer_queue)
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", streaming=True, callbacks=[streaming_handler])

    # Creating the custom callback handler class  
    class StreamingHandler(BaseCallbackHandler):  
        def __init__(self, queue) -> None:  
            super().__init__()  
            # we will be providing the streamer queue as an input  
            self._queue = queue  
            # defining the stop signal that needs to be added to the queue in  
            # case of the last token  
            self._stop_signal = None  
            print("Custom handler Initialized")  
        
        # On the arrival of the new token, we are adding the new token in the   
        # queue  
        def on_llm_new_token(self, token: str, **kwargs) -> None:  
            self._queue.put(token)  
    
        # on the start or initialization, we just print or log a starting message  
        def on_llm_start( self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any ) -> None:  
            """Run when LLM starts running."""  
            print("generation started")  
    
        # On receiving the last token, we add the stop signal, which determines  
        # the end of the generation  
        def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:  
            """Run when LLM ends running."""  
            print("\n\ngeneration concluded")  
            self._queue.put(self._stop_signal)

    def set_invoke(self, object, input_variables):
        self.object = object
        self.input_variables = input_variables
    
    def _invoke(self):
        self.object.invoke(self.input_variables)

    def _start_generation(self):  
        # Creating a thread with generate function as a target  
        thread = Thread(target=self._invoke)  
        # Starting the thread  
        thread.start()    

    async def response_generator(self):  
        # Start the generation process  
        self._start_generation()  
    
        # Starting an infinite loop  
        while True:  
            # Obtain the value from the streamer queue  
            value = self.streamer_queue.get()  
            # Check for the stop signal, which is None in our case  
            if value == None:  
                # If stop signal is found break the loop  
                break  
            # Else yield the value  
            yield value  
            # statement to signal the queue that task is done  
            self.streamer_queue.task_done()  
    
            # guard to make sure we are not extracting anything from   
            # empty queue  
            await asyncio.sleep(0.1)


'''
# 활용 코드 
%other_file.py
from fastapi import FastAPI  
from fast_langchain import StreamingWrapper
from fastapi.responses import StreamingResponse  
from langchain_core.output_parsers import StrOutputParser

app = FastAPI()  

streaming_wrapper = StreamingWrapper()
# chain/agent 정의
chain = prompt | streaming_wrapper.llm | StrOutputParser()
streaming_wrapper.set_invoke(object=chain, input_variables={"si_data": state["si_data"]})

@app.get('/query-stream/')  
async def stream(query: str):  
    print(f'Query receieved: {query}')  
    return StreamingResponse(streaming_wrapper.response_generator(query), media_type='text/event-stream')
'''
