import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, Depends
from exceptions import UnicornException
from tracker.models import User, UserInput 

# Users -------------------
    
def create_or_login(db: Session, data: UserInput):
    db_user = db.query(User).filter(User.email == data.email).first()
    if db_user:
        return db_user
    db_user = User(username=data.username, email=data.email, role='user')
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
    
def delete_user(db: Session, id: str):
    try:
        db_user = db.query(User).filter(User.id == id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(db_user)
        db.commit()
        return "Deleted"
    except Exception as e:
        db.rollback()
        raise UnicornException(name=str(e))

    
def query_user(db: Session, email: str):
    try: 
        user = db.query(User).filter(User.email == email).first()
        return user
    except Exception as e:
        db.rollback()
        raise UnicornException(name=str(e))

