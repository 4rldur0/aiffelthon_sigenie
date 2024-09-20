from langchain_openai import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Initialize OpenAI Chat Model (GPT-4)
llm = ChatOpenAI(temperature=0, 
                 model_name="gpt-4o-mini",
                 streaming=True,              
                 callbacks=[StreamingStdOutCallbackHandler()]
                )
