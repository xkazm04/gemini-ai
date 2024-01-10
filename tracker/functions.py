from sqlalchemy.orm import Session
from tracker.models import User, Note, Completed, NoteInput, TaskInput, Task, TaskUpdate, NoteUpdate, CompInput
from tracker.models import HabitTemplateInput, HabitTemplate, HabitInput, Habit, Categories
from tracker.models import Countdown, CountdownCreate,TimerCreate, Timer
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from exceptions import UnicornException
from crud.templates import create_model, update_model, delete_model, get_filtered_items
from datetime import datetime, timedelta

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
            specific_days=data.specificDays,
            volume_start = data.volume_start,
            volume_units = data.volume_units,
            volume_actual = data.volume_start,
        )
        db.add(db_habit)
        db.commit()
        db.refresh(db_habit)
        return db_habit
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def get_user_habits(db: Session, user: str):
    try:
        db_user = db.query(User).filter(User.id == user).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
        return db.query(Habit).filter(Habit.user_id == db_user.id).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def get_user_daily_habits(db: Session, user: str, day: str):
    try:
        db_user = db.query(User).filter(User.id == user).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
        # Convert the date string to a datetime object
        date = datetime.strptime(day, "%Y-%m-%d")
        # Get the day of the week (0 = Monday, 6 = Sunday)
        day_of_week = date.weekday()
        # Filter habits based on the day of the week
        return db.query(Habit).filter(Habit.user_id == db_user.id).filter(Habit.specific_days[day_of_week] == True).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))

def delete_habit(db: Session, habit_id: str):
    delete_model(db=db, model=Habit, id=habit_id)


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

def delete_habit_template(db: Session, temp: str):
    return delete_model(db=db, model=HabitTemplate, id=temp)
    
def create_habit_from_template(db: Session, temp: str):
    try:
        db_temp = db.query(HabitTemplate).filter(HabitTemplate.id == temp).first()
        db_habit = Habit(
            user_id=db_temp.creator, 
            name=db_temp.name,
            day_type=db_temp.day_type, 
            category=db_temp.category, 
            date_from=db_temp.date_from, 
            date_to=db_temp.date_to, 
            is_recurring=db_temp.is_recurring, 
            recurrence_type=db_temp.recurrence_type, 
            recurrence_interval=db_temp.recurrence_interval, 
            specific_days=db_temp.specific_days,
            type = db_temp.type,
            volume_start = db_temp.volume_start,
            volume_units = db_temp.volume_units,
            volume_target = db_temp.volume_target,
            volume_actual = db_temp.volume_actual,
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
        db_habit = db.query(Habit).filter(Habit.id == habit).first()
        if not db_habit:
            raise HTTPException(status_code=400, detail="Habit not found")
        notes = db.query(Note).filter(Note.habit_id == db_habit.id).all()
        return notes
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def get_user_notes(db: Session, user: str):
    try:
        db_user = db.query(User).filter(User.id == user).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
        habits = get_user_habits(db=db, user=user)
        notes = []
        for habit in habits:
            note = db.query(Note).filter(Note.habit_id == habit.id).all()
            notes.append(note)
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
    delete_model(db=db, model=Note, id=id)
    
# Tasks ----------------------
def create_task(db: Session, data: TaskInput):
    try:
        today = datetime.now()
        db_task = Task(user_id=data.user_id, habit_id=data.habit_id, name=data.name, created_at=today, completed=False)
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
        if data.name is not None:
            db_task.name = data.name
        if data.completed is not None:
            db_task.completed = data.completed
        db.commit()
        db.refresh(db_task)
        return db_task
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
    
def get_user_tasks(db: Session, user: str):
    return get_filtered_items(db=db, model=Task, filter_model=User, id=user, filter_column="user_id")

def get_habit_tasks(db: Session, habit: str):
    return get_filtered_items(db=db, model=Task, filter_model=Habit, id=habit, filter_column="habit_id")
    

# Completion ------------------

def create_completion(db: Session, data: CompInput):
    try:
        db_comp = Completed(habit_id=data.habit_id, day=data.day, volume_actual=data.volume_actual, volume_units=data.volume_units)
        db.add(db_comp)
        db.commit()
        db.refresh(db_comp)
        return db_comp
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def update_completion(db: Session, data: CompInput):
    try:
        db_comp = db.query(Completed).filter(Completed.habit_id == data.habit_id).filter(Completed.day == data.day).first()
        if (db_comp):
            db_comp.completed = data.completed
            db.commit()
            db.refresh(db_comp)
            return db_comp
        else:
            return create_completion(db=db, data=data)
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def get_day_completions(db: Session, habit_id: str, day: str):
    try:
        db_comp = db.query(Completed).filter(Completed.habit_id == habit_id).filter(Completed.day == day).first()
        return db_comp
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def get_week_completions(db: Session, habit_id: str):
    try:
        last_week = datetime.now() - timedelta(days=5)
        db_comp = db.query(Completed).filter(Completed.habit_id == habit_id).all()
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
        completions = []
        for habit in habits:
            db_habit = db.query(Habit).filter(Habit.id == habit).first()
            if not db_habit:
                raise HTTPException(status_code=400, detail="Habit not found")
            completion = db.query(Completed).filter(Completed.habit_id == db_habit.id).all()
            completions.append(completion)
        return completions
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def get_categories(db: Session):
    try:
        categories = db.query(Categories).all()
        if not categories:
            raise HTTPException(status_code=400, detail="Categories not found")
        return categories
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
        
