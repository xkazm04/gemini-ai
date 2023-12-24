import nest_asyncio
nest_asyncio.apply()
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Postgres
from database import SessionLocal
from models import File 

from llama_index import (
    LLMPredictor,
    GPTVectorStoreIndex, 
    GPTListIndex, 
    GPTSimpleKeywordTableIndex,
    download_loader
)

from llama_index.text_splitter import SentenceSplitter

from llama_index.node_parser import SimpleNodeParser
from llama_index.storage.docstore import MongoDocumentStore
from llama_index.storage.index_store import MongoIndexStore
from llama_index.storage.storage_context import StorageContext
from llama_index.node_parser.file import SimpleFileNodeParser
from llama_index import SimpleDirectoryReader
from llama_index.readers.file.flat_reader import FlatReader
from llama_index.readers.file.markdown_reader import MarkdownReader
from llama_index.node_parser import SentenceSplitter
from llama_index import Document
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
from pathlib import Path
import os

# Add nodes to MongoDB backed Docstore
MONGO_URI = os.environ["MONGO_URI"]
MONGODB_DATABASE = "gpt4_paper"
MONGODB_DB_YAML = "demo_openapi"
MONGODB_DB_PDF = "demo_pdf"
MONGODB_DB_MD = "demo_md"
docstore=MongoDocumentStore.from_uri(uri=MONGO_URI, db_name=MONGODB_DATABASE)

text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)

def i(documents, storage_context):
    # Split document into nodes
    nodes = text_splitter.get_nodes_from_documents(documents)
    docstore=MongoDocumentStore.from_uri(uri=MONGO_URI, db_name=MONGODB_DATABASE)
    docstore.add_documents(nodes)
    # Vectorize nodes
    # The list index is a simple data structure where nodes are stored in a sequence. 
    # During index construction, the document texts are chunked up, converted to nodes, and stored in a list.
    GPTListIndex(nodes, storage_context=storage_context)
    # An index that that is built on top of an existing vector store.
    # https://gpt-index.readthedocs.io/en/v0.6.0/reference/indices/vector_store.html
    GPTVectorStoreIndex(nodes, storage_context=storage_context) 
    GPTSimpleKeywordTableIndex(nodes, storage_context=storage_context) 
    print(nodes)
    print('indexed')

def vector_load(id):
    docstore= None
    storage_context = None
    db=SessionLocal()
    documents = []
    db_file = db.query(File).filter(File.id == id).first()
    type = db_file.type
    if db_file.embed == True:
        print('already embedded')
        return 
    elif type == 'yaml':
        # Loading documents to memory
        PDFReader = download_loader("PDFReader")
        pdf_loader = PDFReader()
        storage_context = StorageContext.from_defaults(
            docstore=docstore,
            index_store=MongoIndexStore.from_uri(uri=MONGO_URI, db_name=MONGODB_DB_YAML),
        )
        with open('temp.yaml', 'wb') as f:
            f.write(db_file.binary_data)
        document = Document(
            text= db_file.binary_data.decode('utf-8'),
            metadata={
                'filename': db_file.name,
                'category': 'custom category',
                'language': 'en'
            }
        )
        reader = FlatReader()
        # documents = SimpleDirectoryReader("temp.yaml", filename_as_id=True).load_data()
        documents = reader.load_data(Path('temp.yaml'))  
        i(documents, storage_context)
        os.remove('temp.yaml')
    elif type == 'application/pdf':
        storage_context = StorageContext.from_defaults(
            docstore=docstore,
            index_store=MongoIndexStore.from_uri(uri=MONGO_URI, db_name=MONGODB_DB_PDF),
        )
       # Write the binary data to a PDF file
        with open('output.pdf', 'wb') as f:
            f.write(db_file.binary_data)
        # Load the PDF into a memory
        documents = pdf_loader.load_data(file='output.pdf')
        # Vectorize nodes to the store
        i(documents, storage_context)
        # Clean up file from disk
        os.remove('output.pdf')
    return documents

def read_vectors(q):
    storage_context = StorageContext.from_defaults(
        docstore=MongoDocumentStore.from_uri(uri=MONGO_URI, db_name=MONGODB_DATABASE),
        index_store=MongoIndexStore.from_uri(uri=MONGO_URI, db_name=MONGODB_DATABASE),
    )
    docstore=MongoDocumentStore.from_uri(uri=MONGO_URI, db_name=MONGODB_DATABASE)
    nodes = list(docstore.docs.values())
    len(docstore.docs)
    vector_index = GPTVectorStoreIndex(nodes, storage_context=storage_context) 
    vector_response = vector_index.as_query_engine().query(q) 
    return vector_response

# query_engine_tools = [
#     QueryEngineTool (
#         query_engine=simple_query_engine,
#         metadata=ToolMetadata(
#             name="Simple query engine",
#             description="Simple query engine that uses the vector store index",
#             input=ToolInput(
#                 type="text",
#                 description="Query text",
#                 name="query",
#             ),
#             output=ToolOutput(
#                 type="text",
#                 description="Query response",
#                 name="response",
#             ),
#         ),
#     )
# ]

# query_engine = SubQuestionQueryEngine.from_defaults(
#     query_engine_tools=query_engine_tools,
# )

# Metadata filtering
# query_engine = index.as_query_engine(
#     filters = MetadataFilters(
#         filters=[ExactMatchFilter(key="category", value="custom category")]
#     )
# )

# Vector index auto-retrieval