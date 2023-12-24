from fastapi import status, UploadFile, APIRouter, HTTPException, File as FastAPIFile
from models import File as FileModel
from sqlalchemy.orm import Session
from database import SessionLocal
from file_processor.yaml_indexer import read_vectors, vector_load
from file_processor.file_store import get_file, post_file, update_file_embed_status

router = APIRouter()

@router.get("/file", status_code=status.HTTP_200_OK)
async def get_all_files():
    files = get_file(db=SessionLocal())
    if len(files) == 0:
        return {"message": "No files"}
    return files

@router.post("/file")
async def create_file(file: UploadFile = FastAPIFile(...)):
    try: 
        post_file(db=SessionLocal(), data=file)
        return {"message": "Success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/file/{id}/embed")
async def update_file_embed (id: int):
    try: 
        vector_load(id=id)
        update_file_embed_status(db=SessionLocal(), id=id)
        return {"message": "Success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
# Answer question to the vector store
@router.get("/file/read")
async def index_file(q: str):
    try: 
        answer = read_vectors(q)
        return answer
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/file/vectorize")
async def vec(type: str, fileId: str):
    try: 
        # Create a new session
        db: Session = SessionLocal()
        # Fetch the file from the database
        db_file: FileModel = db.query(FileModel).filter(FileModel.id == fileId).first()
        if not db_file:
            raise HTTPException(status_code=400, detail="File not found")
        # Get the file content
        file_content = db_file.file
        # Pass the file content to the vector_load function
        vector_load(type=type, file_content=file_content)
        return {"message": "Success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/pdf")
async def question_pdf(q: str): 
    try:
        answer = read_vectors(q)
        return answer
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))