
from fastapi import APIRouter, Depends, HTTPException
from tracker.models import UserInput
from auth.functions import create_or_login, query_user, delete_user
from cache.fns import create_redis_user, queue_new_user
from sqlalchemy.orm import Session
from database import SessionLocal

db: Session = SessionLocal()
router = APIRouter()


@router.post("/user/register", status_code=201)
async def register_user(user: UserInput):
    try: 
        request = create_or_login(db=db, data=user)
        return request
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/user/redis/register", status_code=201)
async def register_redis_user(user: UserInput):
    try: 
        queue_new_user(user)
        request = create_redis_user(data=user)
        return request
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 
    
@router.delete("/user/{id}")
async def remove_user(id: str):
    try: 
        request = delete_user(db=db, id=id)
        return request
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
# ------- USER API -------------
    
@router.get("/user/{email}")
async def get_user(email: str):
    user = query_user(db=db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user   
