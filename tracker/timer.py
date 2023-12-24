
from sqlalchemy.orm import Session
from tracker.models import Countdown, CountdownCreate,TimerCreate, Timer, TimeInput, TimeStateInput
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

# Countdown - ✓
def create_countdown(db: Session, data: CountdownCreate):
    try:
        db_cd = Countdown(user_id=data.user_id, countdown=data.countdown,elapsed=0, state='active' )
        db.add(db_cd)
        db.commit()
        db.refresh(db_cd)
        return db_cd
    except IntegrityError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=400, detail="400")

    
def get_user_countdown(db: Session, user_id: str):
    try:
        db_cd = db.query(Countdown).filter(Countdown.user_id == user_id, Countdown.state == 'active').first()
        return db_cd
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="User not found")
    
    
def update_countdown_time(db: Session, id: str, data: TimeInput):
    db_cd = db.query(Countdown).filter(Countdown.id == id).first()
    if db_cd is None:
        raise HTTPException(status_code=404, detail="Countdown not found")
    try:
        db_cd.elapsed = data.elapsed
        db.commit()
        db.refresh(db_cd)
        return db_cd
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to update countdown")
    
def finish_countdown(db: Session, id: str, data: TimeStateInput):
    try:
        db_cd = db.query(Countdown).filter(Countdown.id == id).first()
        db_cd.state = data.state
        db.commit()
        db.refresh(db_cd)
        return db_cd
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Countdown not found")
    
# Timer ---- mimo scope 
# Nový schema, start time, end time 
def create_timer(db: Session, data: TimerCreate):
    try:
        db_timer = Timer(user_id=data.user_id, tracker_id=data.tracker_id, time=data.time)
        db.add(db_timer)
        db.commit()
        db.refresh(db_timer)
        return db_timer
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Tracker not found")
    
    
def get_aggregated_timers_time(db: Session, tracker_id):
    try: 
        db_timer = db.query(Timer).filter(Timer.tracker_id == tracker_id).all()
        total_time = 0
        for timer in db_timer:
            total_time += timer.time
        return total_time
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Tracker not found")
    
def get_all_timers(db: Session, user_id):
    try: 
        db_timer = db.query(Timer).filter(Timer.user_id == user_id).all()
        return db_timer
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Tracker not found")
    
