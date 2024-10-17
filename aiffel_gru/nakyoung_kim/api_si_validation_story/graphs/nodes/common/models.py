from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

gpt_4o_mini = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

gemini_1_5_flash = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.0)

