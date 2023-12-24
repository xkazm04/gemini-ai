
from sqlalchemy.orm import Session
from tracker.models import User, Note, Completed, NoteInput, TaskInput, Task, TaskUpdate, NoteUpdate, CompInput
from tracker.models import HabitTemplateInput, HabitTemplate, HabitInput, Habit
from tracker.models import Countdown, CountdownCreate,TimerCreate, Timer
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, Depends
from exceptions import UnicornException

# Habits ----------------
def create_habit(db: Session, data: HabitInput):
    try:
        db_habit = Habit(
            user_id=data.userId, 
            name=data.name,
            day_type=data.dayType, 
            category=data.category, 
            date_from=data.dateFrom, 
            date_to=data.dateTo, 
            is_recurring=data.isRecurring, 
            recurrence_type=data.recurrenceType, 
            recurrence_interval=data.recurrenceInterval, 
            specific_days=data.specificDays
        )
        db.add(db_habit)
        db.commit()
        db.refresh(db_habit)
        return db_habit
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def get_user_habits(db: Session, user: str):
    db_user = db.query(User).filter(User.id == user).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db.query(Habit).filter(Habit.user_id == db_user.id).all()


def create_habit_template(db: Session, data: HabitTemplateInput):
    try:
        db_habit = HabitTemplate(
            name=data.name,
            description=data.description,
            day_type=data.dayType, 
            category=data.category, 
            date_from=data.dateFrom, 
            date_to=data.dateTo, 
            is_recurring=data.isRecurring, 
            recurrence_type=data.recurrenceType, 
            recurrence_interval=data.recurrenceInterval, 
            specific_days=data.specificDays,
            type = data.type,
            volume_start = data.volumeStart,
            volume_units = data.volumeUnits,
            volume_target = data.volumeTarget,
            volume_actual = data.volumeActual,
            creator = data.creator
        )
        db.add(db_habit)
        db.commit()
        db.refresh(db_habit)
        return db_habit
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))

def delete_habit_template(db: Session, id: str):
    try:
        db_habit = db.query(HabitTemplate).filter(HabitTemplate.id == id).first()
        db.delete(db_habit)
        db.commit()
        return db_habit
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def create_habit_from_template(db: Session, data: HabitTemplate):
    try:
        db_habit = Habit(
            user_id=data.creator, 
            name=data.name,
            day_type=data.day_type, 
            category=data.category, 
            date_from=data.date_from, 
            date_to=data.date_to, 
            is_recurring=data.is_recurring, 
            recurrence_type=data.recurrence_type, 
            recurrence_interval=data.recurrence_interval, 
            specific_days=data.specific_days
        )
        db.add(db_habit)
        db.commit()
        db.refresh(db_habit)
        return db_habit
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))


# Habit notes ---------------

def get_habit_notes(db: Session, habit: str):
    try:
        db.begin()
        db_habit = db.query(Habit).filter(Habit.id == habit).first()
        if not db_habit:
            raise HTTPException(status_code=400, detail="Habit not found")
        notes = db.query(Note).filter(Note.habit_id == db_habit.id).all()
        db.commit()
        return notes
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
    
def create_note(db: Session, data: NoteInput):
    try:
        db_note = Note(habit_id=data.habitId, note_created=data.created, text=data.text, ai=data.ai)
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))

def update_note(db: Session, id: str, data: NoteUpdate):
    try:
        db_note = db.query(Note).filter(Note.id == id).first()
        db_note.text = data.text
        db.commit()
        db.refresh(db_note)
        return db_note
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def delete_note_by_id(db: Session, id: str):
    try:
        db_note = db.query(Note).filter(Note.id == id).first()
        db.delete(db_note)
        db.commit()
        return db_note
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
# Tasks ----------------------
def create_task(db: Session, data: TaskInput):
    try:
        db_task = Task(user_id=data.user_id, habit_id=data.habit_id, name=data.name, created_at=data.created_at)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def update_task(db: Session, id: str, data: TaskUpdate):
    try:
        db_task = db.query(Task).filter(Task.id == id).first()
        db_task.completed = data.completed
        db.commit()
        db.refresh(db_task)
        return db_task
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def get_user_tasks(db: Session, user: str):
    db_user = db.query(User).filter(User.id == user).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db.query(Task).filter(Task.user_id == db_user.id).all()

def get_habit_tasks(db: Session, habit: str):
    db_habit = db.query(Habit).filter(Habit.id == habit).first()
    if not db_habit:
        raise HTTPException(status_code=400, detail="Habit not found")
    return db.query(Task).filter(Task.habit_id == db_habit.id).all()
    

# Completion ------------------

def create_completion(db: Session, data: CompInput):
    try:
        db_comp = Completed(habit_id=data.habit_id, day=data.day)
        db.add(db_comp)
        db.commit()
        db.refresh(db_comp)
        return db_comp
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def update_completion(db: Session, id: str, data: CompInput):
    try:
        db_comp = db.query(Completed).filter(Completed.id == id).first()
        db_comp.completed = data.completed
        db.commit()
        db.refresh(db_comp)
        return db_comp
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
    
def get_habit_completions(db: Session, habit: str):
    db_habit = db.query(Habit).filter(Habit.id == habit).first()
    if not db_habit:
        raise HTTPException(status_code=400, detail="Habit not found")
    return db.query(Completed).filter(Completed.habit_id == db_habit.id).all()

def get_habits_completions(db: Session, habits: list):
    try:
        db.begin()
        completions = []
        for habit in habits:
            db_habit = db.query(Habit).filter(Habit.id == habit).first()
            if not db_habit:
                raise HTTPException(status_code=400, detail="Habit not found")
            completion = db.query(Completed).filter(Completed.habit_id == db_habit.id).all()
            completions.append(completion)
        db.commit()
        return completions
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
