# Receive email, parse specific data
# Identiy requirements, reply if something is missing
# Apply memory. Try to achieve all required data
# Save data to database
# try using SummaryIndex!

from llama_index import SummaryIndex
from llama_index.langchain_helpers.memory_wrapper import GPTIndexChatMemory

# Import things that are needed generically
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from dotenv import load_dotenv
load_dotenv()

# Prompt templates
from langchain.prompts import PromptTemplate
from langchain.chains.openai_functions import create_openai_fn_chain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
import json



email_example = {
    "sender": "mkazdan@seznam.cz",
    "receiver": "milan@seznam.cz",
    "subject": "Documents for the bank",
    "body": "Please activate ID 55 for Administration module",
}

    
class EmailOutput(BaseModel):
    """Parse email content to structured db format."""
    module: str = Field(..., description="Application module parsed from the email")
    fee_id: int = Field(..., description="Fee ID parsed from the email")
    
parser = PydanticOutputParser(pydantic_object=EmailOutput)

    
response_schemas = [
    ResponseSchema(
        name="module",
        description="Application module parsed from the email",
        type="string",
    ),
    ResponseSchema(
        name="fee_id",
        description="Fee ID parsed from the email",
        type="integer",
    ),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()



def parse_email(body: str):
    email = {
        "body": body,
        "sender": "mkazdan@seznam.cz",
        "receiver": "milan@seznam.cz",
        "subject": "Documents for the bank",
    }
    return json.dumps(email)

functions = [
    {
        "name": "parse_email",
        "description": "Parse email content to structured db format",
        "parameters": {
            "type": "object",
            "properties": {
                "sender": {
                    "type": "string",
                    "description": "Sender of the eamil",
                },
                "subject": {
                    "type": "string",
                    "description": "Subject of the eamil",
                },
                "body": {
                    "type": "string",
                    "description": "Body of the eamil",
                },
            },
            "required": ["body"],
        },
    }
]

class EmailInput(BaseModel):
    """Parse email content to structured db format."""
    sender: str = Field(..., description="Sender of the eamil") 
    subject: str = Field(..., description="Subject of the eamil") 
    body: str = Field(..., description="Body of the eamil")

pydantic_classes = [EmailOutput]

llm = ChatOpenAI()
temp = """You are an AI chatbot processing email inputs from human. The goal is to parse email content to structured JSON format.

Email to parse is: {email_input}
"""

prompt_parsed = PromptTemplate(
    template=temp,
    input_variables=["email_input"],
    # partial_variables={"format_instructions": parser.get_format_instructions()}, --- does not work from some reason
)

prompt = PromptTemplate(input_variables=["email input"], template=temp,
   # partial_variables={"format_instructions": parser.get_format_instructions()}
)


def email_request(body: str):
    chain = create_openai_fn_chain(pydantic_classes, llm, prompt, verbose=True)
    output = chain.run(body)
    print(output)
    return output




