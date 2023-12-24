
from fastapi import APIRouter, Depends, HTTPException
from tracker.models import UserInput
from auth.functions import create_user, query_user
from cache.fns import create_redis_user, queue_new_user
from sqlalchemy.orm import Session
from database import SessionLocal
from pydantic import BaseModel



class User (BaseModel):
    username: str

db: Session = SessionLocal()
router = APIRouter()


@router.post("/user/register", status_code=201)
async def register_user(user: UserInput):
    try: 
        request = create_user(db=db, data=user)
        print(request)
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
    
    
# ------- USER API ---------
@router.post("/tracker/user")
async def user_create(user: User):
    try: 
        request = create_user(db=db, data=user.username)
        return request
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/tracker/user")
async def get_user(username: str):
    user = query_user(db=db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user   
