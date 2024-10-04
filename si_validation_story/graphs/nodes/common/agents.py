from .tools import *
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

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
    def __init__(self, prompt, llm):
        self.search = TavilySearchResults(k=5)
        self.llm = llm
        self.prompt = PromptTemplate.from_template(prompt)
        self.PDF_retriever_tool = self.retrieve_documents()
        self.rag_agent, self.tools = self.create_agent()

    def retrieve_documents(self):
        # ======
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(current_dir, "cherry_comliance.pdf")
        # ======
        PDF_loader = PyPDFLoader(pdf_path)
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, length_function=len, separators=["\n\n", "\n", " ", ""])
        PDF_split_docs = PDF_loader.load_and_split(text_splitter)
        
        embeddings = OpenAIEmbeddings()
        
        PDF_vector = FAISS.from_documents(documents=PDF_split_docs, embedding=embeddings)
        
        PDF_retriever = PDF_vector.as_retriever()
        
        PDF_retriever_tool = create_retriever_tool(
            PDF_retriever,
            name="pdf_search",
            description="Use this tool for compliance for shipper, consignee, and notifyParty" \
                        "including checking what info is required for each entity" \
                        "based on the requirements of both the company and relevant countries",
        )
        
        return PDF_retriever_tool

    def create_agent(self):
        tools = [self.search, self.PDF_retriever_tool]
        agent = create_openai_functions_agent(self.llm, tools, self.prompt)
        return agent, tools

    def generate_response(self, si_data):
        agent_executor = AgentExecutor(agent=self.rag_agent, tools=self.tools, verbose=True)
        result = agent_executor.invoke({'si_data': si_data})
        return result

    def invoke(self, si_data):
        response = self.generate_response(si_data)
        return response