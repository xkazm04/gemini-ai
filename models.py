from pydantic import BaseModel, Field
from sqlalchemy.types import LargeBinary
from sqlalchemy import  Column, Enum as SQLEnum, Integer, String
from sqlalchemy.types import Boolean
from database import Base

class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True, index=True)
    todo = Column(String)

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String)
    binary_data = Column(LargeBinary)
    name = Column(String)
    size = Column(Integer)
    embed = Column(Boolean, default=False)
    
class Question(BaseModel):
    question: str

    
class EmailOutput(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    module: str = Field(..., description="Application module parsed from the email")
    fee_id: int = Field(..., description="Fee ID parsed from the email")
    
class EmailInput(BaseModel):
    """Parse email content to structured db format."""
    # sender: str = Field(..., description="Sender of the eamil") 
    # subject: str = Field(..., description="Subject of the eamil") 
    text: str = Field(..., description="Body of the eamil")