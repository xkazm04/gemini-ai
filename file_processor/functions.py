

from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import initialize_agent
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.agents import Tool
from langchain.chains import RetrievalQA
from pydantic import BaseModel, Field

# Llama Index
import os
import nest_asyncio
nest_asyncio.apply()
import logging
import sys
from llama_index import (
    LLMPredictor,
    GPTVectorStoreIndex, 
    GPTListIndex, 
    GPTSimpleKeywordTableIndex,
    download_loader
)
from langchain.chat_models import ChatOpenAI
from llama_index.response.notebook_utils import display_response
from llama_index.node_parser import SimpleNodeParser
import requests
from pathlib import Path
from llama_index import VectorStoreIndex, SimpleDirectoryReader


from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

tools = []

class DocumentInput(BaseModel):
    question: str = Field()
    
# Use google drive as data source
# https://python.langchain.com/docs/integrations/toolkits/google_drive
def gdrive():
    pass


# API - Req, question + file  
def process_csv(question,file):
    llm = OpenAI(temperature=0)
    agent = create_csv_agent(llm=llm, csv_path=file, verbose=True, agent_type=AgentType.OPENAI_FUNCTIONS,)
    return agent.run(question)

# Doc compare
# https://python.langchain.com/docs/integrations/toolkits/document_comparison_toolkit
def compare_docs(files):
   
    pass

def compare_apis():
# https://python.langchain.com/docs/integrations/toolkits/openapi    
    pass


def llama_read_pdf():
    PDFReader = download_loader("PDFReader")
    loader = PDFReader()

    out_dir = Path("data")
    if not out_dir.exists():
        os.makedirs(out_dir)
    out_path = out_dir / "paper.pdf"
        
    if not out_path.exists():
        url = 'https://arxiv.org/pdf/2303.08774.pdf'
        r = requests.get(url)
        with open(out_path, 'wb') as f:
            f.write(r.content)
            
    doc = loader.load_data(file=Path(out_path))[0]
    nodes = SimpleNodeParser().get_nodes_from_documents([doc])
    list_index = GPTListIndex(nodes, storage_context=storage_context)
    vector_index = GPTVectorStoreIndex(nodes, storage_context=storage_context)
    keyword_table_index = GPTSimpleKeywordTableIndex(nodes, storage_context=storage_context)
