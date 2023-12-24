import bcrypt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, Depends
from exceptions import UnicornException
from tracker.models import User, UserInput 

# Users -------------------
def create_user(db: Session, data: UserInput):
    db_user = db.query(User).filter(User.username == data.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="A user with this username already exists.")
    db_user = db.query(User).filter(User.email == data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="A user with this email already exists.")
    hashed_password = get_password_hash(data.password)
    db_user = User(username=data.username, email=data.email, role='user', hashed_password=hashed_password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def query_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password: str) -> str:
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return password_hash.decode()

def protected_route(token: str = Depends(oauth2_scheme)):
    return {"token": token}

def get_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    return user

def fake_decode_token(token):
    return get_user(token)

def get_me(current_user: User = Depends(get_user)):
    return current_user

def user_validate_role (current_user: User = Depends(get_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return current_user

def login(db: Session, form_data: OAuth2PasswordRequestForm = Depends()):
    user = query_user(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())