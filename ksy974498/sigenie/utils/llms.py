from langchain_openai import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm(llm_name):
    # Initialize OpenAI Chat Model (GPT-4)
    if llm_name == "gpt-4o-mini":
        llm = ChatOpenAI(temperature=0, 
                    model_name="gpt-4o-mini",
                    streaming=True,              
                    callbacks=[StreamingStdOutCallbackHandler()]
                    )
    # elif llm_name == "gemini-1.5-flash":
    #     llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.0)
    
    # ========== 다른 모델 더 추가 가능 ==========

    return llm
