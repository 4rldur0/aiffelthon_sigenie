from .tools import *
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_openai_functions_agent, AgentExecutor

class BasicChain:
    def __init__(self, llm, prompt, input_variables):
        # Initialize your LLM
        self.llm = llm
        
        # Setup the prompt template and chain
        self.prompt = PromptTemplate(template=prompt, input_variables=input_variables)
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def __call__(self, *args, **kwargs):
        return self.chain(*args, **kwargs)
    
    def invoke(self, *args, **kwargs):
        return self.chain.invoke(*args, **kwargs)
    
# Build Retrieval-Augmented Generation Pipeline
class RAGAgent:
    def __init__(self, prompt, llm, pdf_path, vector_name):
        self.llm = llm
        self.prompt = PromptTemplate.from_template(prompt)
        PDF_retriever_tool = Faiss.retrieve_pdf(pdf_path, vector_name)
        web_search_tool = Tavily.web_search()    # default: k=5
        self.tools = [PDF_retriever_tool, web_search_tool]

    def _generate_response(self, si_data):
        agent = create_openai_functions_agent(self.llm, self.tools, self.prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        result = agent_executor.invoke({'si_data': si_data})
        return result

    def invoke(self, si_data):
        response = self._generate_response(si_data)
        return response