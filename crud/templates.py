from sqlalchemy.orm import Session
from exceptions import UnicornException
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import Type, List
from database import Base

def create_model(db: Session, model: Type[Base], data: dict) -> Base:
    try:
        instance = model(**data)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def get_model_by_id(db: Session, model: Type[Base], id: str) -> Base:
    instance = db.query(model).filter(model.id == id).first()
    if not instance:
        raise HTTPException(status_code=400, detail=f"{model.__name__} not found")
    return instance

def update_model(db: Session, model: Type[Base], id: str, data: dict) -> Base:
    try:
        db.query(model).filter(model.id == id).update(data)
        db.commit()
        return get_model_by_id(db, model, id)
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def delete_model(db: Session, model: Type[Base], id: str) -> str:
    instance = get_model_by_id(db, model, id)
    try:
        db.delete(instance)
        db.commit()
        return "deleted"
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def get_filtered_items(db: Session, model: Type[Base], filter_model: Type[Base], id: str, filter_column: str):
    db_item = db.query(filter_model).filter(filter_model.id == id).first()
    if not db_item:
        raise HTTPException(status_code=400, detail=f"{filter_model.__name__} not found")
    return db.query(model).filter(getattr(model, filter_column) == db_item.id).all()